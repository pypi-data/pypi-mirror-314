from typing import List
from sqlalchemy import func, select, or_, orm

from caerp.controllers.task.estimation import EstimationInvoicingController
from caerp.models.project.business import BusinessPaymentDeadline
from caerp.models.task import Task, Invoice, Estimation, CancelInvoice


def gen_invoice_from_payment_deadline(
    request,
    business,
    payment_deadline,
    add_estimation_details=False,
):
    controller = EstimationInvoicingController(payment_deadline.estimation, request)
    if payment_deadline.deposit:
        invoice = controller.gen_deposit_invoice(
            request.identity,
            payment_deadline.description,
            payment_deadline.amount_ttc,
            date=payment_deadline.date,
            add_estimation_details=add_estimation_details,
        )
    elif payment_deadline in get_sold_deadlines(request, business):
        return gen_sold_invoice(request, business, payment_deadline)
    else:
        invoice = controller.gen_intermediate_invoice(
            request.identity,
            payment_deadline.description,
            payment_deadline.amount_ttc,
            date=payment_deadline.date,
            add_estimation_details=add_estimation_details,
        )
    payment_deadline.invoice_id = invoice.id
    request.dbsession.merge(payment_deadline)
    return invoice


def gen_new_intermediate_invoice(request, business, add_estimation_details=False):
    """
    Generate an intermediate invoice not related to a payment deadline
    """
    controller = EstimationInvoicingController(business.estimations[-1], request)
    invoice = controller.gen_intermediate_invoice(
        request.identity,
        "Nouvelle facture",
        0,
        add_estimation_details=add_estimation_details,
    )
    return invoice


def gen_sold_invoice(
    request, business, payment_deadline=None, ignore_previous_invoices=False
):
    if payment_deadline is None:
        payment_deadline = business.payment_deadlines[-1]
    controller = EstimationInvoicingController(payment_deadline.estimation, request)
    invoice = controller.gen_sold_invoice(
        request.identity,
        date=payment_deadline.date,
        ignore_previous_invoices=ignore_previous_invoices,
    )
    payment_deadline.invoice_id = invoice.id
    request.dbsession.merge(payment_deadline)
    return invoice


def currently_invoicing(request, business):
    query = (
        select(func.count(Task.id))
        .where(Task.type_.in_(Task.invoice_types))
        .where(Task.business_id == business.id)
        .where(Task.status != "valid")
    )

    return request.dbsession.execute(query).scalar() != 0


def find_payment_deadline_by_id(request, business, deadline_id):
    """Return the payment deadline with the given id attached to the business"""
    return (
        request.dbsession.query(BusinessPaymentDeadline)
        .filter_by(business_id=business.id)
        .filter_by(id=deadline_id)
        .first()
    )


def get_deadlines_by_estimation(
    request, business
) -> List[List[BusinessPaymentDeadline]]:
    """
    Group a business' payment deadlines by estimation
    """
    result = {}
    query = (
        select(BusinessPaymentDeadline)
        .join(BusinessPaymentDeadline.estimation)
        .where(BusinessPaymentDeadline.business_id == business.id)
        .order_by(
            Estimation.date,
            BusinessPaymentDeadline.deposit.desc(),
            BusinessPaymentDeadline.order,
        )
    )
    for deadline in request.dbsession.execute(query).scalars():
        result.setdefault(deadline.estimation_id, []).append(deadline)
    return list(result.values())


def get_estimation_deadlines(request, estimation) -> List[BusinessPaymentDeadline]:
    query = (
        select(BusinessPaymentDeadline)
        .where(BusinessPaymentDeadline.estimation_id == estimation.id)
        .order_by(BusinessPaymentDeadline.deposit.desc(), BusinessPaymentDeadline.order)
    )
    return request.dbsession.execute(query).scalars().all()


def get_deposit_deadlines(request, business) -> List[BusinessPaymentDeadline]:
    """Return the deposit payment deadline of a business"""
    query = select(BusinessPaymentDeadline).where(
        BusinessPaymentDeadline.business_id == business.id,
        BusinessPaymentDeadline.deposit == True,
    )
    return request.dbsession.execute(query).scalars().all()


def get_intermediate_deadlines(request, business) -> List[BusinessPaymentDeadline]:
    """Collect the intermediate payment deadlines of a business"""
    result = []
    for deadlines in get_deadlines_by_estimation(request, business):
        result.extend([deadline for deadline in deadlines[:-1] if not deadline.deposit])
    return result


def get_sold_deadlines(request, business) -> List[BusinessPaymentDeadline]:
    """Collect the sold payment deadlines of a business"""
    return [a[-1] for a in get_deadlines_by_estimation(request, business) if len(a) > 0]


def _get_amount_to_invoice(request, business, estimation=None, mode="ht"):
    polymorphic_task = orm.with_polymorphic(Task, [Invoice, CancelInvoice])
    invoiced_query = select(func.sum(getattr(polymorphic_task, mode))).where(
        Task.business_id == business.id,
        Task.type_.in_(Task.invoice_types),
    )
    if estimation:
        # On restreint à un devis et aux factures qui le concerne
        estimated = getattr(estimation, mode)
        invoice_alias = orm.aliased(Invoice)
        invoiced_query = invoiced_query.outerjoin(
            invoice_alias, polymorphic_task.CancelInvoice.invoice_id == invoice_alias.id
        ).where(
            or_(
                polymorphic_task.Invoice.estimation_id == estimation.id,
                invoice_alias.estimation_id == estimation.id,
            )
        )
    else:
        estimated_query = (
            select(func.sum(getattr(Estimation, mode)))
            .where(Estimation.business_id == business.id)
            .where(Estimation.signed_status != "aborted")
        )
        estimated = request.dbsession.execute(estimated_query).scalar() or 0
    invoiced = request.dbsession.execute(invoiced_query).scalar() or 0

    return int(estimated - invoiced)


def get_amount_to_invoice_ht(request, business, estimation=None):
    """
    Compute the amount to invoice for this business
    if an estimation is provided, restrict to the given estimation
    """
    return _get_amount_to_invoice(request, business, estimation, mode="ht")


def get_amount_to_invoice_ttc(request, business, estimation=None):
    """
    Compute the amount to invoice for this business
    if an estimation is provided, restrict to the given estimation
    """
    return _get_amount_to_invoice(request, business, estimation, mode="ttc")


def get_invoices_without_deadline(request, business):
    query = (
        select(Invoice)
        .where(Invoice.business_id == business.id)
        .where(
            Invoice.id.not_in(
                [d.invoice_id for d in business.payment_deadlines if d.invoice_id]
            )
        )
    )

    return request.dbsession.execute(query).scalars().all()


def guess_payment_deadline_from_invoice(request, business, invoice):
    """Try to guess the payment deadline from an invoice"""
    query = (
        select(BusinessPaymentDeadline)
        .where(BusinessPaymentDeadline.business_id == business.id)
        .where(BusinessPaymentDeadline.invoice_id == None)
        .order_by(BusinessPaymentDeadline.order.asc())
    )
    for deadline in request.dbsession.execute(query).scalars():
        if deadline.amount_ttc == invoice.ttc:
            deadline.invoice_id = invoice.id
            if invoice.status == "valid":
                deadline.invoiced = True
            request.dbsession.merge(deadline)
            return deadline
    return None


def get_task_outside_payment_deadline(request, business, min_date=None, max_date=None):
    """
    Collect Task objects not attached to a payment deadline
    """
    query = (
        select(Task)
        .filter(Task.business_id == business.id)
        .filter(
            Task.id.notin_(
                select(BusinessPaymentDeadline.invoice_id).where(
                    BusinessPaymentDeadline.business_id == business.id,
                    BusinessPaymentDeadline.invoice_id != None,
                )
            )
        )
        .order_by(Task.date.desc())
    )
    if min_date:
        query = query.filter(Task.date > min_date)
    if max_date:
        query = query.filter(Task.date <= max_date)
    return request.dbsession.execute(query).scalars().all()
