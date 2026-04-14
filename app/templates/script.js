async function carregarDados() {
    try {
        const response = await fetch('../../app/data/data11.json');


        const dados = await response.json();
        console.log("Resposta da requisição:", dados);

        // Exemplo de uso: acessando uma propriedade do JSON
        console.log("O ID do desenvolvimento é:", dados.development_id);
        return dados;

    } catch (erro) {
        console.error("Erro na requisição:", erro);
    }
}




async function exibirDados() {
    const container = document.getElementById('lista-container');

    try {
        const dados = await carregarDados(); // Sua função que faz o fetch

        // Montando o HTML acessando as propriedades específicas do seu JSON
        let html = `
            <div class="card">
                <h2>${dados.group.name}</h2>
                <p><strong>Código do Grupo:</strong> ${dados.group.code}</p>
                <p><em>${dados.group.reasoning}</em></p>
                
                <hr>
                
                <h3>Atividade: ${dados.activity.description}</h3>
                <p><strong>Código:</strong> ${dados.activity.code}</p>
                
                <div class="info-box">
                    <strong>Modalidade:</strong> ${dados.modalidade.modality_name} (${dados.modalidade.modality_acronym})<br>
                    <strong>Classe:</strong> ${dados.porte.result_class}
                </div>

                <h4>Faixas de Produção:</h4>
                <ul>
        `;

        // Aqui sim usamos forEach, porque 'size_ranges' é uma lista dentro do objeto!
        dados.activity.size_ranges.forEach(faixa => {
            html += `
                <li>
                    Porte ${faixa.size_category}: 
                    ${faixa.min_value || '0'} a ${faixa.max_value || '∞'} ${faixa.measurement_unit}
                </li>`;
        });

        html += `
                </ul>
            </div>
        `;

        container.innerHTML = html;

    } catch (erro) {
        console.error("Erro ao renderizar:", erro);
        container.innerHTML = "<p>Erro ao carregar os dados.</p>";
    }
}

exibirDados();
