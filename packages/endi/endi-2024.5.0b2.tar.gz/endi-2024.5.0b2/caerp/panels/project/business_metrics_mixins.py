from caerp.models.project.mixins import BusinessMetricsMixin


def business_metrics_totals(
    context,
    request,
    instance: BusinessMetricsMixin,
    tva_on_margin: bool,
):
    return dict(instance=instance, tva_on_margin=tva_on_margin)


def includeme(config):
    config.add_panel(
        business_metrics_totals,
        "business_metrics_totals",
        renderer="caerp:templates/panels/project/business_metrics_totals.mako",
    )
