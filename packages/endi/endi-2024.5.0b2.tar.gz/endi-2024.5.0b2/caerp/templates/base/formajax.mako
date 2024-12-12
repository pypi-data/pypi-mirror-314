% if not message is UNDEFINED:
    <div class='text-center'>
        <div id='msg-div' class="alert alert-success" tabindex='1'>
          <button class="icon only unstyled close" title="Masquer ce message" aria-label="Masquer ce message" data-dismiss="alert" type="button"><svg><use href="${request.static_url('caerp:static/icons/endi.svg')}#times"></use></svg></button>
          <span class="icon"><svg><use href="${request.static_url('caerp:static/icons/endi.svg')}#success"></use></svg></span> 
          ${api.clean_html(message)|n}
        </div>
      </div>
% endif
% if not form is UNDEFINED:
    ${form|n}
% endif
<script type='text/javascript'>
    $('#msg-div').focus();
</script>
