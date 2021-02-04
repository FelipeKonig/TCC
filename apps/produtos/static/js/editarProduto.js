function editarProduto(id){
        Swal.fire({
          title: 'Atenção!',
          text: "Tem certeza que deseja editar o seu produto?",
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
              id = document.getElementsByName("campoIDProduto"+id)[0].value;

            $.ajax({
                type: 'POST',
                url: '/produtos/editar-produto/',
                data: {
                    csrfmiddlewaretoken: token,
                    id: id
                },
                success: function(result){
                    window.location.href = '/produtos/editar-produto/';
                }
            });
          }
        })
}

