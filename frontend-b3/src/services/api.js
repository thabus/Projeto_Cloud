// src/services/api.js

// É SÓ PARA TESTAR ENQUANTO NÃO CONECTAMOS NA AZURE FUNCTION!!!!

// ⚠️ TODO: DEPOIS SUBSTITUIR PELA URL DA SUA AZURE FUNCTION
const API_URL = "http://localhost:7071/api/GetB3Data"; 

export const buscarDadosAcoes = async () => {
    try {
        // --- MODO DE DESENVOLVIMENTO (DADOS FALSOS) ---
        // Enquanto não conectamos na Azure, usamos isso para testar a tela
        return [
            { ticker: "VALE3", trade_date: "2025-10-23", close_price: "68.50", min_price: "67.00", max_price: "69.00" },
            { ticker: "PETR4", trade_date: "2025-10-23", close_price: "34.20", min_price: "33.80", max_price: "34.90" },
            { ticker: "ITUB4", trade_date: "2025-10-23", close_price: "31.00", min_price: "30.50", max_price: "31.50" },
            { ticker: "WEGE3", trade_date: "2025-10-23", close_price: "40.10", min_price: "39.50", max_price: "40.80" }
        ];

        // --- MODO REAL (QUANDO FOR CONECTAR) ---
        // const response = await fetch(API_URL);
        // if (!response.ok) throw new Error('Erro ao buscar dados');
        // return await response.json();
        
    } catch (error) {
        console.error("Erro na API:", error);
        return [];
    }
};