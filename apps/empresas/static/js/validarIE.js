$(document).ready(function(){

  $("#id_inscricaoEstadual").change(function() {

    let ie = CheckIE(this.value);

    if(ie == false){
      document.getElementById("id_inscricaoEstadual").style.borderColor = "red";
      $("#id_inscricaoEstadual").val('');
    }else{
      document.getElementById("id_inscricaoEstadual").style.borderColor = "#ced4da";
    }

  });

  $("#estado").change(function() {

    let ie = CheckIE($("#id_inscricaoEstadual").val());

    if(ie == false){
      document.getElementById("id_inscricaoEstadual").style.borderColor = "red";
      $("#id_inscricaoEstadual").val('');
    }else{
      document.getElementById("id_inscricaoEstadual").style.borderColor = "1px solid #ced4da";
    }

  });

  function CheckIE(ie){

     estado = document.getElementById('estado').value;
     // onde Txt_UF é o ID da UF de seu formulário

     ie = ie.replace(/\./g, "");
     ie = ie.replace(/\\/g, "");
     ie = ie.replace(/\-/g, "");
     ie = ie.replace(/\//g, "");

     if ( ie == "ISENTO" )
        return true;

     switch(estado){

     case "AC":

          if (ie.length != 13)
             return false;
          var b = 4, soma = 0;
          for (var i=0; i<=10; i++)
          {
              soma += parseInt(ie.charAt(i)) * b;
              --b;
              if (b == 1)
  			   b = 9;
          }
          dig = 11 - (soma % 11);
          if (dig >= 10)
  		   dig = 0;
          if (dig != parseInt(ie.charAt(11)))
  		   return false;
          b = 5;
          soma = 0;
          for (var i=0; i<=11; i++)
          {
              soma += parseInt(ie.charAt(i)) * b;
              --b;
              if (b == 1)
  			   b = 9;
          }
          dig = 11 - (soma % 11);
          if (dig >= 10)
  		   dig = 0;
          return (dig == parseInt(ie.charAt(12)));
          break;

     case "AL":

          if (ie.length != 9)
             return false;
          var b = 9, soma = 0;
          for (var i=0; i<=7; i++)
          {
              soma += parseInt(ie.charAt(i)) * b;
              --b;
          }
          soma *= 10;
          dig = soma - (Math.floor(soma / 11) * 11);
          if (dig == 10)
  		   dig = 0;
          return (dig == parseInt(ie.charAt(8)));
          break;

     case "AM":

          if (ie.length != 9)
             return false;
          var b = 9, soma = 0;
          for (var i=0; i<=7; i++)
          {
              soma += parseInt(ie.charAt(i)) * b;
              b--;
          }
          if (soma < 11)
  		{
  		   dig = 11 - soma;
          }
          else
          {
             i = soma % 11;
             if (i <= 1)
  		   {
  			  dig = 0;
  		   }
  		   else
  		   {
  			  dig = 11 - i;
  		   }
          }
          return (dig == parseInt(ie.charAt(8)));
          break;

     case "AP":

          if (ie.length != 9)
             return false;
  		if (ie.substring(0,2) != "03")
  		   return false;
          var p = 0, d = 0, i = ie.substring(1,8);
          if ((i >= 3000001) && (i <= 3017000))
          {
             p =5;
             d = 0;
          }
          else if ((i >= 3017001) && (i <= 3019022))
          {
             p = 9;
             d = 1;
          }
          b = 9;
          soma = p;
          for (var i=0; i<=7; i++)
          {
              soma += parseInt(ie.charAt(i)) * b;
              b--;
          }
          dig = 11 - (soma % 11);
          if (dig == 10)
          {
             dig = 0;
          }
          else if (dig == 11)
          {
             dig = d;
          }
          return (dig == parseInt(ie.charAt(8)));
          break;

     case "BA":

          if (ie.length == 8)
  		{
             die = ie.substring(0, 8);
             var nro = new Array(8);
             var dig = -1;
             for (var i=0; i<=7; i++)
                 nro[i] = parseInt(die.charAt(i));
             var NumMod = 0;
             if (String(nro[0]).match(/[0123458]/))
  	       {
                NumMod = 10;
  		   }
             else
  		   {
                NumMod = 11;
  		   }
  		   b = 7;
             soma = 0;
             for (i=0; i<=5; i++)
             {
                 soma += nro[i] * b;
                 b--;
             }
             i = soma % NumMod;
             if (NumMod == 10)
             {
                if (i == 0) { dig = 0; } else { dig = NumMod - i; }
             }
             else
             {
                if (i <= 1) { dig = 0; } else { dig = NumMod - i; }
             }
             resultado = (dig == nro[7]);
             if (!resultado)
  	          return false;
             b = 8;
             soma = 0;
             for (i=0; i<=5; i++)
             {
                 soma += nro[i] * b;
                 b--;
             }
             soma += nro[7] * 2;
             i = soma % NumMod;
             if (NumMod == 10)
             {
                if (i == 0) { dig = 0; } else { dig = NumMod - i; }
             }
             else
             {
                if (i <= 1) { dig = 0; } else { dig = NumMod - i; }
             }
             return (dig == nro[6]);
  		}

          if (ie.length == 9)
  		{
             die = ie.substring(0, 9);
             var nro = new Array(9);
             var dig = -1;
             for (var i=0; i<=8; i++)
                 nro[i] = parseInt(die.charAt(i));
             var NumMod = 0;
             if (String(nro[0]).match(/[0123458]/))
             {
                NumMod = 10;
  		   }
             else
  	       {
                NumMod = 11;
  	       }
  	       b = 8;
             soma = 0;
             for (i=0; i<=6; i++)
             {
                 soma += nro[i] * b;
                 b--;
             }
             i = soma % NumMod;
             if (NumMod == 10)
             {
                if (i == 0) { dig = 0; } else { dig = NumMod - i; }
             }
             else
             {
                if (i <= 1) { dig = 0; } else { dig = NumMod - i; }
             }
             resultado = (dig == nro[8]);
             if (!resultado)
                return false;
             b = 9;
             soma = 0;
             for (i=0; i<=6; i++)
             {
                 soma += nro[i] * b;
                 b--;
             }
             soma += nro[8] * 2;
             i = soma % NumMod;
             if (NumMod == 10)
             {
                if (i == 0) { dig = 0; } else { dig = NumMod - i; }
             }
             else
             {
                if (i <= 1) { dig = 0; } else { dig = NumMod - i; }
             }
             return (dig == nro[7]);
  		}

  		return false;
  		break;

     case "CE":

          if (ie.length != 9)
             return false;
  		die = ie;
          var nro = Array(9);
          for (var i=0; i<=8; i++)
              nro[i] = parseInt(die[i]);
          b = 9;
          soma = 0;
          for (i=0; i<=7; i++)
          {
              soma += nro[i] * b;
              b--;
          }
          dig = 11 - (soma % 11);
          if (dig >= 10)
             dig = 0;
          return (dig == nro[8]);
          break;

     case "DF":

          if (ie.length != 13)
             return false;
          var nro = new Array(13);
          for (var i=0; i<=12; i++)
              nro[i] = parseInt(ie.charAt(i));
          b = 4;
          soma = 0;
          for (i=0; i<=10; i++)
          {
              soma += nro[i] * b;
              b--;
              if (b == 1)
                 b = 9;
          }
          dig = 11 - (soma % 11);
          if (dig >= 10)
             dig = 0;
          if (dig != nro[11])
             return false;
          b = 5;
          soma = 0;
          for (i=0; i<=11; i++)
          {
              soma += nro[ i ] * b;
              b--;
              if (b == 1)
                 b = 9;
          }
          dig = 11 - (soma % 11);
          if (dig >= 10)
             dig = 0;
          return (dig == nro[12]);
          break;

     case "ES":

          if (ie.length != 9)
             return false;
          var nro = new Array(9);
          for (var i=0; i<=8; i++)
              nro[i] = parseInt(ie.charAt(i));
          b = 9;
          soma = 0;
          for (i=0; i<=7; i++)
          {
              soma += nro[i] * b;
              b--;
          }
          i = soma % 11;
          if (i < 2) { dig = 0; } else { dig = 11 - i; }
          return (dig == nro[8]);
          break;

     case "GO":

          if (ie.length != 9)
             return false;
          s = ie.substring(0, 2);
          if ((s == '10') || (s == '11') || (s == '15'))
          {
             var nro = new Array(9);
             for (var i=0; i<=8; i++)
                 nro[i] = parseInt(ie.charAt(i));
             //n = Math.floor(ie / 10);
             n = parseInt(ie.substring(0, 7));
             if (n = 11094402)
             {
                if ((nro[8] == 0) || (nro[8] == 1))
                   return true;
             }
             b = 9;
             soma = 0;
             for (i=0; i<=7; i++)
             {
                 soma += nro[i] * b;
                 b--;
             }
             i = soma % 11;
             if (i == 0)
                dig = 0;
             else
             {
                if (i == 1)
                {
                    if ((n >= 10103105) && (n <= 10119997))
                       dig = 1;
                    else
                       dig = 0;
                }
                else
                    dig = 11 - i;
             }
             return (dig == nro[8]);
          }
          return false;
          break;

     case "MA":

          if (ie.length != 9)
             return false;
          if ( ie.substring(0, 2) != "12" )
  		   return false;
          var nro = new Array(9);
          for (var i=0; i<=8; i++)
              nro[i] = parseInt(ie.charAt(i));
          b = 9;
          soma = 0;
          for (i=0; i<=7; i++)
          {
              soma += nro[i] * b;
              b--;
          }
          i = soma % 11;
          if (i <= 1) { dig = 0; } else { dig = 11 - i; }
          return (dig == nro[8]);
          break;

     case "MG":

          if (ie.length != 13)
             return false;
          dig1 = ie.substring(11, 12);
          dig2 = ie.substring(12, 13);
          inscC = ie.substring(0, 3) + '0' + ie.substring(3, 11);
          insc = inscC.split('');
          npos = 11;
          i = 1;
          ptotal = 0;
          psoma = 0;
          while (npos >= 0)
          {
                i++;
                psoma = parseInt(insc[npos]) * i;
                if (psoma >= 10)
                   psoma -= 9;
                ptotal += psoma;
                if (i == 2)
                   i = 0;
                npos--;
          }
          nresto = ptotal % 10;
          if (nresto == 0)
             nresto = 10;
          nresto = 10 - nresto;
          if (nresto != parseInt(dig1))
             return false;
          npos = 11;
          i = 1;
          ptotal = 0;
          is=ie.split('');
          while (npos >= 0)
          {
                i++;
                if (i == 12)
                   i = 2;
                ptotal += parseInt(is[npos]) * i;
                npos--;
          }
          nresto = ptotal % 11;
          if ((nresto == 0) || (nresto == 1))
             nresto = 11;
          nresto = 11 - nresto;
          return (nresto == parseInt(dig2));
  		break;

     case "MS":

          if (ie.length != 9)
             return false;
          if (ie.substring(0,2) != "28")
             return false;
          var nro = new Array(9);
          for (var i=0; i<=8; i++)
              nro[i] = parseInt(ie.charAt(i));
          b = 9;
          soma = 0;
          for (i=0; i<=7; i++)
          {
              soma += nro[i] * b;
              b--;
          }
          i = soma % 11;
          if (i <= 1) { dig = 0; } else { dig = 11 - i; }
          return (dig == nro[8]);
          break;

     case "MT":

          if (ie.length != 11)
             return false;
          die = ie;
          var nro = new Array(11);
          for (var i=0; i<=10; i++)
              nro[i] = parseInt(die[i]);
          b = 3;
          soma = 0;
          for (i=0; i<=9; i++)
          {
              soma += nro[i] * b;
              b--;
              if (b == 1)
                 b = 9;
          }
          i = soma % 11;
          if (i <= 1) { dig = 0; } else { dig = 11 - i; }
          return (dig == nro[10]);
          break;

     case "PA":

          if (ie.length != 9)
             return false;
          if (ie.substring(0, 2) != '15')
             return false;
          var nro = new Array(9);
          for (var i=0; i<=8; i++)
              nro[i] = parseInt(ie.charAt(i));
          b = 9;
          soma = 0;
          for (i=0; i<=7; i++)
          {
              soma += nro[i] * b;
              b--;
          }
          i = soma % 11;
          if (i <= 1)
             dig = 0;
          else
             dig = 11 - i;
          return (dig == nro[8]);
          break;

     case "PB":

          if (ie.length != 9)
             return false;
          var nro = new Array(9);
          for (var i=0; i<=8; i++)
              nro[i] = parseInt(ie.charAt(i));
          b = 9;
          soma = 0;
          for (i=0; i<=7; i++)
          {
              soma += nro[i] * b;
              b--;
          }
          i = soma % 11;
          if (i <= 1)
             dig = 0;
          else
             dig = 11 - i;
          return (dig == nro[8]);
          break;

     case "PE":

          // IE antiga com 14 digitos
          if (ie.length == 14)
          {
             var nro = new Array(14);
             for (var i=0; i<=13; i++)
                 nro[i] = parseInt(ie.charAt(i));
             b = 5;
             soma = 0;
             for (i=0; i<=12; i++)
             {
                 soma += nro[i] * b;
                 b--;
                 if (b == 0)
                    b = 9;
             }
             dig = 11 - (soma % 11);
             if (dig > 9)
                dig = dig - 10;
             return (dig == nro[13]);
  		}

          // IE nova com 9 digitos
          if (ie.length == 9)
          {
  		   var nro = new Array(9);
             for (var i=0; i<=8; i++)
                 nro[i] = parseInt(ie.charAt(i));
             b = 8;
             soma = 0;
             for (i=0; i<=6; i++)
             {
                 soma += nro[i] * b;
                 b--;
             }
             i = soma % 11;
             if (i <= 1) { dig = 0; } else { dig = 11 - i; }
             if (dig != nro[7])
                return false;
             b = 9;
             soma = 0;
             for (i=0; i<=7; i++)
             {
                 soma += nro[i] * b;
                 b--;
             }
             i = soma % 11;
             if (i <= 1) { dig = 0; } else { dig = 11 - i; }
             return (dig == nro[8]);
  		}

  		return false;
  		break;

     case "PI":

          if (ie.length != 9)
             return false;
          var nro = new Array(9);
          for (var i=0; i<=8; i++)
              nro[i] = parseInt(ie.charAt(i));
          b = 9;
          soma = 0;
          for (i=0; i<=7; i++)
          {
              soma += nro[i] * b;
              b--;
          }
          i = soma % 11;
          if (i <= 1) { dig = 0; } else { dig = 11 - i; }
          return (dig == nro[8]);
          break;

     case "PR":

          if (ie.length != 10)
             return false;
          var nro = new Array(10);
          for (var i=0; i<=9; i++)
              nro[i] = parseInt(ie.charAt(i));
          b = 3;
          soma = 0;
          for (i=0; i<=7; i++)
          {
              soma += nro[i] * b;
              b--;
              if (b == 1)
                 b = 7;
          }
          i = soma % 11;
          if (i <= 1)
             dig = 0;
          else
             dig = 11 - i;
          if (dig != nro[8])
             return false;
          b = 4;
          soma = 0;
          for (i=0; i<=8; i++)
          {
              soma += nro[i] * b;
              b--;
              if (b == 1)
                 b = 7;
          }
          i = soma % 11;
          if (i <= 1)
             dig = 0;
          else
             dig = 11 - i;
          return (dig == nro[9]);
          break;

     case "RJ":

          if (ie.length != 8)
             return false;
          var nro = new Array(8);
          for (var i=0; i<=7; i++)
              nro[i] = parseInt(ie.charAt(i));
          b = 2;
          soma = 0;
          for (i=0; i<=6; i++)
          {
              soma += nro[i] * b;
              b--;
              if (b == 1)
                 b = 7;
          }
          i = soma % 11;
          if (i <= 1) { dig = 0; } else { dig = 11 - i; }
          return (dig == nro[7]);
          break;

     case "RN":

          if (ie.substring(0, 2) != '20')
             return false;

          // IE com 9 digitos
  		if (ie.length == 9)
          {
             var nro = new Array(9);
             for (var i=0; i<=8; i++)
                 nro[i] = parseInt(ie.charAt(i));
             b = 9;
             soma = 0;
             for (i=0; i<=7; i++)
             {
                 soma += nro[i] * b;
                 b--;
             }
             soma *= 10;
             dig = soma % 11;
             if (dig == 10)
                dig = 0;
             return (dig == nro[8]);
  		}

          // IE com 10 digitos
          if (ie.length == 10)
          {
             var nro = new Array(10);
             for (var i=0; i<=9; i++)
                 nro[i] = parseInt(ie.charAt(i));
             b = 10;
             soma = 0;
             for (i=0; i<=8; i++)
             {
                 soma += nro[i] * b;
                 b--;
             }
             soma *= 10;
             dig = soma % 11;
             if (dig == 10)
                dig = 0;
             return (dig == nro[9]);
  		}

          return false;
  		break;

     case "RO":

          if (ie.length != 14)
             return false;
          var nro = new Array(14);
          b=6;
          soma=0;
          for (var i=0; i <= 12; i++)
  		{
              nro[i] = parseInt(ie.charAt(i));
              soma += nro[i] * b;
              b--;
              if (b == 1)
                 b = 9;
          }
          dig = 11 - ( soma % 11);
          if (dig >= 10)
             dig = dig - 10;
          return (dig == parseInt(ie.charAt(13)));
          break;

     case "RR":

          if (ie.length != 9)
             return false;
          if (ie.substring(0,2) != "24")
             return false;
          var nro = new Array(9);
          for (var i=0; i<=8; i++)
              nro[i] = parseInt(ie.charAt(i));
          var soma = 0;
          var n = 0;
          for (i=0; i<=7; i++)
              soma += nro[ i ] * ++n;
          dig = soma % 9;
          return (dig == nro[8]);
          break;

     case "RS":

          if (ie.length != 10)
             return false;
          var nro = new Array(10);
          for (var i=0; i<=9; i++)
              nro[i] = parseInt(ie.charAt(i));
          b = 2;
          soma = 0;
          for (i=0; i<=8; i++)
          {
              soma += nro[i] * b;
              b--;
              if (b == 1)
                  b = 9;
          }
          dig = 11 - (soma % 11);
          if (dig >= 10)
             dig = 0;
          return (dig == nro[9]);
          break;

     case "SC":

          if (ie.length != 9)
             return false;
          var nro = new Array(9);
          for (var i=0; i<=8; i++)
              nro[i] = parseInt(ie.charAt(i));
          b = 9;
          soma = 0;
          for (i=0; i<=7; i++)
          {
              soma += nro[i] * b;
              b--;
          }
          i = soma % 11;
          if (i <= 1)
             dig = 0;
          else
             dig = 11 - i;
          return (dig == nro[8]);
          break;

     case "SE":

          if (ie.length != 9)
             return false;
          var nro = new Array(9);
          for (var i=0; i<=8; i++)
              nro[i] = parseInt(ie.charAt(i));
          b = 9;
          soma = 0;
          for (i=0; i<=7; i++)
          {
              soma += nro[i] * b;
              b--;
          }
          dig = 11 - (soma % 11);
          if (dig >= 10)
             dig = 0;
          return (dig == nro[8]);
          break;

     case "SP":

          if (ie.length != 12)
             return false;
          var nro = new Array(12);
          for (var i=0; i<=11; i++)
  	        nro[i] = parseInt(ie.charAt(i));
          soma = (nro[0] * 1) + (nro[1] * 3) + (nro[2] * 4) + (nro[3] * 5) + (nro[4] * 6) + (nro[5] * 7) + (nro[6] * 8) + (nro[7] * 10);
          dig = soma % 11;
          if (dig >= 10)
  	       dig = 0;
          if (dig != nro[8])
             return false;
          soma = (nro[0] * 3) + (nro[1] * 2) + (nro[2] * 10) + (nro[3] * 9) + (nro[4] * 8) + (nro[5] * 7) + (nro[6] * 6)  + (nro[7] * 5) + (nro[8] * 4) + (nro[9] * 3) + (nro[10] * 2);
          dig = soma % 11;
          if (dig >= 10)
  	       dig = 0;
          return (dig == nro[11]);
          break;

     case "TO":

          if (ie.length != 11)
             return false;
  		s = ie.substring(2,4);
          if ((s != "01") && (s != "02") && (s != "03") && (s != "99"))
  		   return false;
  		var nro = new Array(11);
          b=9;
          soma=0;
          for (var i=0; i<=9; i++)
          {
              nro[i] = parseInt(ie.charAt(i));
              if( i != 2 && i != 3)
  			{
                 soma += nro[i] * b;
                 b--;
              }
          }
          resto = soma % 11;
          if ( resto < 2 ) { dig = 0; } else { dig = 11 - resto; }
          return (dig == parseInt(ie.charAt(10)));
          break;

     default:
          return false;

     }
  }
});
