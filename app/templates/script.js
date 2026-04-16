

const API_URL = 'http://127.0.0.1:8000/api/v1/licenciamento';

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
                e_ia:true
            })
        });
        
        if (!response.ok) throw new Error(`Erro: ${response.status}`);

        const dados = await response.json();
        
        if (dados.id && dados.description) {
            console.log("Descrição do empreendimento:", dados.description);
            
            
            window.location.href = `teste2.html?id=${dados.id}&name=${dados.name}&description=${(dados.description)}`;
        }
        else
        {            console.error("Resposta inesperada da API:", dados);
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


    formData.append('development_id', id);
    formData.append('user_input', description);

    
    const inputArquivo = document.getElementById('documents');
    if (inputArquivo.files[0]) {
        formData.append('document', inputArquivo.files[0]);
    }

    try {
        const response = await fetch(`${API_URL}/api/licensing/ai/inputs/`, {
            method: 'POST',
            body: formData
        });

        const resultado = await response.json();
         window.location.href = `teste3.html?id=${id}&name=${name}&description=${(description)}`;
        console.log("Sucesso:", resultado);
    } catch (error) {
        console.error("Erro ao enviar:", error);
    }
}

async function getclassificacao(event) {
    // Se a função for chamada por um evento, isso impede qualquer reload
    if (event) event.preventDefault(); 

    console.log("Iniciando...");
    const resultadoDiv = document.getElementById('resultado');
    resultadoDiv.innerText = "Carregando..."; // Feedback visual pro usuário

    try {
        const response = await fetch(`${API_URL}/api/licensing/ai/classify/full`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ "development_id": 12 })
        });

        if (!response.ok) throw new Error(`Status: ${response.status}`);
        
        const dados = await response.json();
        
        // Renderiza o resultado
        resultadoDiv.innerText = `Grupo ${dados.group} - Atividade: ${dados.activity} - Classificação: ${dados.classification}`;
        document.body.style.color = "#fff";

    } catch (error) {
        console.error("Erro na requisição:", error);
        resultadoDiv.innerText = "Erro ao buscar classificação. Verifique o console.";
    }
}

function getDadosDaURL() 
{
const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
const id = urlParams.get('id');
const description = urlParams.get('description');
const name = urlParams.get('name');
console.log("ID capturado da URL:", id);
console.log("Descrição capturada da URL:", description);
console.log("Nome capturado da URL:", name);
return {"id": id, "name": name, "description": description};
}
