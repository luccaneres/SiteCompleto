// Envia usuario e senha para a API de login
async function fazerLogin() {
    const resposta = await fetch("/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        usuario: document.getElementById("usuario").value,
        senha: document.getElementById("senha").value,
      }),
    });
    const dados = await resposta.json();
  
    if (dados.ok) {
      // Esconde o login e mostra o cadastro
      document.getElementById("area-login").style.display = "none";
      document.getElementById("area-cadastro").style.display = "block";
    } else {
      document.getElementById("msg-login").textContent = "Usuario ou senha invalidos";
    }
  }
  
  // Envia um novo evento para a API (so' funciona se estiver logado)
  async function cadastrarEvento() {
    // datetime-local devolve "2025-08-12T19:00"; trocamos o T por espaco
    const dataHora = document.getElementById("data_hora").value.replace("T", " ");

    let link = document.getElementById("link").value.trim();
    if (link && !link.startsWith("http://") && !link.startsWith("https://")) {
    link = "https://" + link;
    }
  
    const resposta = await fetch("/api/eventos", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        titulo: document.getElementById("titulo").value,
        palestrante: document.getElementById("palestrante").value,
        local: document.getElementById("local").value,
        link: document.getElementById("link").value,
        data_hora: dataHora,
      }),
    });
  
    if (resposta.ok) {
      document.getElementById("msg-cadastro").textContent = "Evento cadastrado!";
    } else {
      document.getElementById("msg-cadastro").textContent = "Erro ao cadastrar.";
    }
  }