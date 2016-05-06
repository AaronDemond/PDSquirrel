// navigates to the selected societys
function navigateSociety() {
  var selected = $("#society-select option:selected").val();
  var pd_id = $('#pd_id').val();
  var url = "/pd/accred/" + pd_id + "/" + selected + "/";
  window.location.href = url;
}
