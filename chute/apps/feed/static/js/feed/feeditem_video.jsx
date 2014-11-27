/** @jsx React.DOM */
var form = $('form#video-feeditem-form');
var form_button = $('form#video-feeditem-form input[type=submit]');
var original_form_button_value = form_button.val();
var video_url_field = $(form.find('#id_video_url'));

var onMessage = function () {

}
var onProgress = function ( progress, percent_string ) {
  // disable
  form_button.attr("disabled", "disabled")
  form_button.val('Uploading ' + percent_string)
}
var onUploadDone = function ( data ) {
  // save the url
  if ( data.status == 200 ) {
    // reset to enabled
    video_url_field.val(data.responseURL);
    form_button.val(original_form_button_value)
    form_button.removeAttr("disabled")
  }
}
var onCancel = function () {
  video_url_field.val('');
  form_button.val(original_form_button_value)
  form_button.removeAttr("disabled")
}

React.render(
  <VideoUploaderView
                uploader_config={UploaderConfig}
                onUploadDone={onUploadDone}
                onProgress={onProgress}
                onCancel={onCancel}
                onMessage={onMessage} />,
  document.getElementById('placeholder-feeditem_video')
);