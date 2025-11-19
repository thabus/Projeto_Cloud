import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend
} from "recharts";
import { format, parseISO } from "date-fns"; 

function GraficoAcoes({ dados }) {
  
  // Proteção: Se não tiver dados, não renderiza nada para não quebrar
  if (!dados || dados.length === 0) {
    return null;
  }

  // IMPORTANTE: Ordena os dados por data. 
  // Se vier fora de ordem, o gráfico de linha vira um rabisco confuso.
  const dadosOrdenados = [...dados].sort((a, b) => {
    return new Date(a.trade_date) - new Date(b.trade_date);
  });

  return (
    <div style={{ width: "100%", height: "100%", minHeight: 300 }}>
      <h3 style={{ textAlign: 'center', color: '#555', margin: '0 0 10px 0', fontSize: '16px' }}>
        Evolução do Fechamento
      </h3>
      
      <ResponsiveContainer width="100%" height="90%">
        <LineChart data={dadosOrdenados} margin={{ top: 5, right: 30, left: 0, bottom: 5 }}>
          
          <CartesianGrid strokeDasharray="3 3" vertical={false} />
          
          {/* Eixo X formatado (Dia/Mês) */}
          <XAxis 
            dataKey="trade_date" 
            tickFormatter={(str) => {
              try {
                return format(parseISO(str), "dd/MM"); 
              } catch {
                return str;
              }
            }}
            minTickGap={30} 
            tick={{ fontSize: 12 }}
          />
          
          {/* Eixo Y formatado (R$) e automático */}
          <YAxis 
            domain={['auto', 'auto']} 
            tickFormatter={(valor) => `R$${valor}`} 
            width={80}
            tick={{ fontSize: 12 }}
          />
          
          <Tooltip 
            formatter={(valor) => [`R$ ${parseFloat(valor).toFixed(2)}`, "Fechamento"]}
            labelFormatter={(label) => {
               try {
                 return format(parseISO(label), "dd/MM/yyyy");
               } catch {
                 return label;
               }
            }}
          />
          
          <Legend />

          <Line 
            type="monotone" 
            dataKey="close_price" 
            stroke="#2566cf" 
            strokeWidth={3}
            dot={dadosOrdenados.length < 30 ? { r: 4 } : false} 
            activeDot={{ r: 6 }} 
            name="Preço Fechamento"
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

export default GraficoAcoes;