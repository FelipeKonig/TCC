$("#foto").change(function() {

    var foto = $("#foto").val();

    try {
      var formato = foto.split(".")

      if (formato[1] == undefined) {
        $("#foto").val('');
        return false;
      }

    } catch (e) {
      $("#foto").val('');
      return false;
    }

    if (formato[1] == 'png' || formato[1] == 'jpeg' || formato[1] == 'jpg') {
      return true;
    }else{
      $("#foto").val('');
      return false;
    }
});
