function editarVitrine(id){
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
            window.location.href = "/vitrines/editar-vitrine/"+id;
          }
        })

}
