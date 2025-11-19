const API_URL = "https://funcao-projeto-b3-exchbhepfyekaccc.canadacentral-01.azurewebsites.net/api/GetB3Data";

export const buscarDadosAcoes = async () => {
    try {
        console.log("Buscando dados em:", API_URL); // Log para ajudar a debugar
        
        const response = await fetch(API_URL);
        
        if (!response.ok) {
            throw new Error(`Erro na API: ${response.status}`);
        }
        
        const data = await response.json();
        console.log("Dados recebidos:", data.length, "registros"); // Confirmação no console
        return data;

    } catch (error) {
        console.error("Falha ao buscar dados:", error);
        return []; // Retorna lista vazia para não quebrar a tela
    }
};