const API_URL = 'http://127.0.0.1:8025/api/v1/licenciamento';

async function enviarFormulario() {
    const formData = new FormData();

    id = getDadosDaURL().id || "1";
    name = getDadosDaURL().name || "Empreendimento Exemplo";
    description = getDadosDaURL().description || "Descrição aqui";

    id = id.toString()

    console.log("ID para envio:", id);
    formData.append('development_id', id);
    formData.append('user_input', "davi.santos");


    const inputArquivo = document.getElementById('documents');
    if (inputArquivo.files[0]) {
        formData.append('document', inputArquivo.files[0]);
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