// Funcao que transforma "2025-08-12 19:00" em "12/08/2025, 19:00"
function formatarData(dataISO) {
    // separa data e hora pelo espaco
    const [data, hora] = dataISO.split(" ");
    const [ano, mes, dia] = data.split("-");
    return `${dia}/${mes}/${ano}, ${hora}`;
  }
  
  // Decide o que mostrar na coluna "Onde / Como participar"
  function montarParticipacao(evento) {
    if (evento.link) {
      // Garante que o link tenha http:// ou https:// na frente.
      // Sem isso, o navegador trata "www.google.com" como caminho relativo.
      let url = evento.link;
      if (!url.startsWith("http://") && !url.startsWith("https://")) {
        url = "https://" + url;
      }
      return `<a href="${url}" target="_blank">Acessar transmissao</a>`;
    } else {
      return evento.local || "A definir";
    }
  }

// Busca os eventos na API e desenha a tabela
async function carregarCronograma() {
    // fetch faz o pedido HTTP GET para a nossa API
    const resposta = await fetch("/api/eventos");
    // converte a resposta JSON em uma lista de objetos JavaScript
    const eventos = await resposta.json();
  
    // encontra o corpo da tabela pelo id definido no HTML
    const corpo = document.getElementById("corpo-cronograma");
    corpo.innerHTML = "";  // limpa antes de redesenhar
  
    // para cada evento, cria uma linha <tr> com as colunas
    eventos.forEach(function (evento) {
      const linha = document.createElement("tr");
      linha.innerHTML = `
        <td>${formatarData(evento.data_hora)}</td>
        <td>${evento.titulo}</td>
        <td>${evento.palestrante}</td>
        <td>${montarParticipacao(evento)}</td>
      `;
      corpo.appendChild(linha);  // adiciona a linha na tabela
    });
  }
  
  // Assim que a pagina carrega, busca e mostra o cronograma
  carregarCronograma();