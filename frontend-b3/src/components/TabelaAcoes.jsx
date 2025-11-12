// src/components/TabelaAcoes.jsx
import { useEffect, useState } from 'react';
import { buscarDadosAcoes } from '../services/api';


const TabelaAcoes = () => {
    const [acoes, setAcoes] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const carregarDados = async () => {
            const dados = await buscarDadosAcoes();
            setAcoes(dados);
            setLoading(false);
        };
        carregarDados();
    }, []);

    if (loading) return <p>Carregando dados do pregão...</p>;

    return (
        <div className="container-tabela">
            <h2>Pregão B3 - Dados do Mercado à Vista</h2>
            <table>
                <thead>
                    <tr>
                        <th>Ticker</th>
                        <th>Data</th>
                        <th>Preço Mínimo</th>
                        <th>Preço Máximo</th>
                        <th>Fechamento</th>
                    </tr>
                </thead>
                <tbody>
                    {acoes.map((acao, index) => (
                        <tr key={index}>
                            <td><strong>{acao.ticker}</strong></td>
                            <td>{acao.trade_date}</td>
                            <td className="preco">R$ {acao.min_price}</td>
                            <td className="preco">R$ {acao.max_price}</td>
                            <td className="preco destaque">R$ {acao.close_price}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default TabelaAcoes;