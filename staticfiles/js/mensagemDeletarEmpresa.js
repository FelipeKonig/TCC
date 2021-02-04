function deletarEmpresa(id){
        Swal.fire({
          title: 'Atenção!',
          text: "Tem certeza que deseja deletar a sua empresa?",
          icon: 'warning',
          showCancelButton: true,
          confirmButtonColor: '#FF0000',
          cancelButtonColor: '#000080',
          confirmButtonText: 'Deletar',
          cancelButtonText: 'Cancelar',
          reverseButtons: true
        }).then((result) => {
          if (result.isConfirmed) {

              token = document.getElementsByName("csrfmiddlewaretoken")[0].value;
              id = document.getElementsByName("campoDeletar")[0].value;

            $.ajax({
                type: 'POST',
                url: '/empresas/deletar-empresa/',
                data: {
                    csrfmiddlewaretoken: token,
                    id: id
                },
                success: function(result){
                    window.location.href = "/empresas/deletar-empresa/";
                }
            });
          }
        })

}

