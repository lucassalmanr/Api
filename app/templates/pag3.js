const API_URL = 'http://127.0.0.1:8000/api/v1/licenciamento';

async function getclassificacao(event) {
    event.preventDefault();

    console.log("Iniciando requisição...");
    const resultadoDiv = document.getElementById('resultado');
    resultadoDiv.innerText = "Carregando...";


    let idRaw = getDadosDaURL().id || "1";

    try {
        const response = await fetch(`http://127.0.0.1:8000/api/v1/licenciamento/api/licensing/ai/classify/full`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                "development_id": idRaw.toString(),
            })
        });
        

        // Se o servidor retornar 400, o bloco catch será acionado pelo throw
        if (!response.ok) {
            const erroDetalhado = await response.json().catch(() => ({}));
            console.error("Erro do Servidor:", erroDetalhado);
            throw new Error(`Status: ${response.status}`);
        }

        const dados = await response.json();

        resultadoDiv.innerText = `Grupo ${dados.group} - Atividade: ${dados.activity} - Classificação: ${dados.classification}`;

       

    } catch (error) {
        console.error("Erro na requisição:", error);
        resultadoDiv.innerText = "Erro ao buscar classificação. Verifique o console.";
    }
}