

const API_URL = 'http://127.0.0.1:8025/api/v1/licenciamento';
const path = require('path');


// FUNÇÃO PARA CRIAR (Chame isso apenas no clique de um botão no HTML)
async function criarNovoEmpreendimento() {
    console.log("Iniciando criação de empreendimento...");
    try {
        console.log("Enviando dados para a API...");
        const response = await fetch(`${API_URL}/criar-empreendimento`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                name: document.getElementById('name').value || "Empreendimento Exemplo",
                description: document.getElementById('description').value || "Descrição aqui",
                e_ia: true
            })
        });

        if (!response.ok) throw new Error(`Erro: ${response.status}`);

        const dados = await response.json();
        console.log("Resposta da API:", dados);
        if (dados.id && dados.description) {
            console.log("Descrição do empreendimento:", dados.description);


            window.location.href = `?id=${dados.id}&name=${dados.name}&description=${(dados.description)}`;
        }
        else {
            console.error("Resposta inesperada da API:", dados);
        }
    } catch (error) {
        console.error("Falha ao criar:", error);
    }
}

async function enviarFormulario() {
    const formData = new FormData();

    id = getDadosDaURL().id || "1";
    name = getDadosDaURL().name || "Empreendimento Exemplo";
    description = getDadosDaURL().description || "Descrição aqui";

    id = id.toString()

    console.log("ID para envio:", id);
    formData.append('development_id', id);
    formData.append('user_input', "davi.santos");


    if (Arquivo) {
        formData.append('document', Arquivo);
    }

    formData.append('e_ai', true); // Enviando como string "true" para o backend

    console.log(formData.get('development_id'), formData.get('user_input'), formData.get('document'));
    try {
        const response = await fetch(`${API_URL}/forms`, {
            method: 'POST',
            body: formData
        });

        const resultado = await response.json();
        console.log("Sucesso:", resultado);
    } catch (error) {
        console.error("Erro ao enviar:", error);
    }
}



async function getclassificacao() {
    

    console.log("Iniciando requisição...");
    const resultadoDiv = document.getElementById('resultado');
    resultadoDiv.innerText = "Carregando...";


    let idRaw = getDadosDaURL().id || "1";

    try {
        const response = await fetch(`http://127.0.0.1:8025/api/v1/licenciamento/api/licensing/ai/classify/full`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                "development_id": idRaw
            })
        });
        

        if (!response.ok) {
            const erroDetalhado = await response.json().catch(() => ({}));
            console.error("Erro do Servidor:", erroDetalhado);
            throw new Error(`Status: ${response.status}`);
        }

        const dados = await response.json();

        resultadoDiv.innerText = `Grupo ${dados.group} - Atividade: ${dados.activity} - Classificação: ${dados.classification}`;

        document.body.style.color = "#000000";

    } catch (error) {
        console.error("Erro na requisição:", error);
        resultadoDiv.innerText = "Erro ao buscar classificação. Verifique o console.";
    }
}

function getDadosDaURL() {
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const id = urlParams.get('id');
    const description = urlParams.get('description');
    const name = urlParams.get('name');
    console.log("ID capturado da URL:", id);
    console.log("Descrição capturada da URL:", description);
    console.log("Nome capturado da URL:", name);
    return { "id": id, "name": name, "description": description };
}

function passarDePagina() {
    window.location.href = `teste3.html?id=${id}&name=${name}&description=${(description)}`;
}