function editarEmpresa(){
        Swal.fire({
          title: 'Atenção!',
          text: "Tem certeza que deseja editar a sua empresa?",
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
              id = document.getElementsByName("campo")[0].value;

            $.ajax({
                type: 'POST',
                url: '/empresas/edicao-empresa/',
                data: {
                    csrfmiddlewaretoken: token,
                    id: id
                },
                success: function(result){
                    window.location.href = "/empresas/edicao-empresa/";
                }
            });

            //window.location.href = "/empresas/editar-empresa/"+id;
          }
        })

}

