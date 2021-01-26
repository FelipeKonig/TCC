function deletarVitrine(id){
        Swal.fire({
          title: 'Atenção!',
          text: "Tem certeza que deseja deletar a sua vitrine?",
          icon: 'warning',
          showCancelButton: true,
          confirmButtonColor: '#FF0000',
          cancelButtonColor: '#000080',
          confirmButtonText: 'Deletar',
          cancelButtonText: 'Cancelar',
          reverseButtons: true
        }).then((result) => {
          if (result.isConfirmed) {
                window.location.href = "/vitrines/deletar-vitrine/"+id;
          }
        })

}

