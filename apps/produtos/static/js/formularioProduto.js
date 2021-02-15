$(document).ready(function () {
  id_tabela = 0;

  $(document).on('click','.table-add', function(){

    var tabela = $(this).parents('table');

    var nova_linha = `<tr>
                        <td><input type="text" name="nome_caracteristica-${tabela.attr('id')}" class="form-control" required/></td>
                        <td><input type="text" name="descricao_caracteristica-${tabela.attr('id')}" class="form-control" required/></td>
                        <td class="pt-3-half">
                          <span class="table-up"><a href="#!" class="indigo-text"><i class="fas fa-long-arrow-alt-up"
                                aria-hidden="true"></i></a></span>
                          <span class="table-down"><a href="#!" class="indigo-text"><i class="fas fa-long-arrow-alt-down"
                                aria-hidden="true"></i></a></span>
                        </td>
                        <td>
                          <span class="table-remove"><button type="button"
                              class="btn btn-danger btn-rounded btn-sm my-0">Remover</button></span>
                        </td>
                      </tr>`

   tabela.append(nova_linha);
  });

  $(document).on('click', '.table-remove', function () {

   $(this).parents('tr').detach();
  });

  $(document).on('click', '.table-up', function () {

   var row = $(this).parents('tr');

   if (row.index() === 0) {
     return;
   }

   row.prev().before(row.get(0));
  });

  $(document).on('click', '.table-down', function () {

   var row = $(this).parents('tr');
   row.next().after(row.get(0));
  });

  $(document).on('click','#add_nova_tabela', function(){

    id_tabela += 1;

    var nova_tabela = `<div class="card">
                        <div class="card-body">
                          <div>
                                <label for="titulo_caracteristica-${id_tabela}" style="font-weight:bold;">Título: </label>
                                <input type="text" name="titulo_caracteristica-${id_tabela}" required>
                              </div>
                            </div>
                            <table name='table' id="${id_tabela}" class="table table-bordered table-responsive-lg table-striped text-center">
                              <thead>
                                <tr>
                                  <th class="text-center">Tópico</th>
                                  <th class="text-center">Descrição</th>
                                  <th style="border-right-color: white;"> </th>
                                  <th class="text-center">
                                      <span class="table-add"><a href="#!" class="text-success"><i
                                        class="fas fa-plus fa-2x" aria-hidden="true"></i></a></span>
                                  </th>
                                </tr>
                              </thead>
                              <tbody>
                                <tr>
                                  <td><input type="text" name="nome_caracteristica-${id_tabela}" class="form-control" required/></td>
                                  <td><input type="text" name="descricao_caracteristica-${id_tabela}" class="form-control" required/></td>
                                  <td class="pt-3-half">
                                    <span class="table-up"><a href="#!" class="indigo-text"><i class="fas fa-long-arrow-alt-up"
                                          aria-hidden="true"></i></a></span>
                                    <span class="table-down"><a href="#!" class="indigo-text"><i class="fas fa-long-arrow-alt-down"
                                          aria-hidden="true"></i></a></span>
                                  </td>
                                  <td>
                                    <span class="table-remove"><button type="button"
                                        class="btn btn-danger btn-rounded btn-sm my-0">Remover</button></span>
                                  </td>
                                </tr>
                              </tbody>
                            </table>
                          </div>
                        </div>
                      </div>
                      <div id="tabela_adicional">
                      </div>`;
    $('#tabela_adicional').append(nova_tabela);
  });

  $("#id_preco").keyup(function() {
      return verificaNumero(this.value, "#id_preco");
  });

  $("#id_quantidade").keyup(function() {
    return verificaNumero(this.value, "#id_quantidade");
  });

  function verificaNumero(char, input) {
    if (char == ''){
      $(input).val($(input).slice(0, -1));
      return false;
    }
      return true;
  }

});
