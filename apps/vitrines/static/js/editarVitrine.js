function editarVitrine(){
        Swal.fire({
          title: 'Atenção!',
          text: "Tem certeza que deseja editar a sua vitrine?",
          icon: 'warning',
          showCancelButton: true,
          confirmButtonColor: '#FF0000',
          cancelButtonColor: '#000080',
          confirmButtonText: 'Editar',
          cancelButtonText: 'Cancelar',
          reverseButtons: true
        }).then((result) => {
          if (result.isConfirmed) {
              token = document.getElementsByName("csrfmiddlewaretoken")[0].value;
              id = document.getElementsByName("campoID")[0].value;

              console.log('token', token)
              console.log('id', id)
             $.ajax({
                type: 'POST',
                url: '/vitrines/editar-vitrine/',
                data: {
                    csrfmiddlewaretoken: token,
                    id: id
                },
                success: function(result){
                     window.location.href = "/vitrines/editar-vitrine/";
                }
            });
          }
        })

}
