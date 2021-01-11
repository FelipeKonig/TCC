$(document).ready(function(){
			$("#id_numeroFixo").mask("(00) 0000-0000")
			$("#id_numeroCelular").mask("(00) 0000-00009")
            $("#id_cpf").mask("000.000.000-00")
			$("#id_numeroCelular").blur(function(event){
				if ($(this).val().length == 15){
					$("#id_numeroCelular").mask("(00) 00000-0009")
				}else{
					$("#id_numeroCelular").mask("(00) 0000-00009")
				}
			})

		})


