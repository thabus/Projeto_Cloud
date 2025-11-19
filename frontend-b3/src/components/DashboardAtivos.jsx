import { useState, useEffect } from "react";
import { AppBar, Toolbar, Typography, Box, Paper } from "@mui/material";
import TabelaAcoes from "./TabelaAcoes";
import GraficoAcoes from "./GraficoAcoes";
import { buscarDadosAcoes } from "../services/api";

function DashboardAtivos() {
  const [filtro, setFiltro] = useState({ ativo: "", de: "", ate: "" });
  const [dados, setDados] = useState([]);

  useEffect(() => {
    buscarDadosAcoes().then(setDados);
  }, []);

  const dadosFiltrados = dados.filter(d => (
    d.ticker.toLowerCase().includes(filtro.ativo.toLowerCase()) &&
    (!filtro.de || d.trade_date >= filtro.de) &&
    (!filtro.ate || d.trade_date <= filtro.ate)
  ));

  return (
    <Box sx={{ background: "#f4f6fa", minHeight: "100vh" }}>
      <AppBar position="static" sx={{ background: "#2566cf" }}>
        <Toolbar>
          <Typography variant="h6" sx={{ flexGrow: 1 }}>
            Dashboard de Ativos
          </Typography>
        </Toolbar>
      </AppBar>
      <Box sx={{ mt: 4, width: '100%', display: "flex", justifyContent: "center" }}>
        <Paper sx={{ p: 4, width: "1200px", boxShadow: 3, background: "#fff" }}>
          <Box sx={{ display: "flex", gap: 4, alignItems: "flex-start", width: "100%", justifyContent: "stretch", flexWrap: "wrap" }}>
            
            <Box sx={{ flex: 3, minWidth: '500px' }}>
              <TabelaAcoes
                onFiltro={() => { }}
                filtro={filtro}
                setFiltro={setFiltro}
                dados={dadosFiltrados}
              />
            </Box>

            <Box sx={{ flex: 2, minWidth: 360 }}>
              {/* PROTEÇÃO: Se tiver mais de 200 pontos, NÃO desenha o gráfico para não travar */}
              {dadosFiltrados.length > 0 && dadosFiltrados.length < 200 ? (
                <Paper elevation={3} sx={{ p: 2, width: '100%', height: 400 }}>
                    <GraficoAcoes dados={dadosFiltrados} />
                </Paper>
              ) : (
                <Paper 
                  elevation={0} 
                  variant="outlined" 
                  sx={{ height: 400, display: 'flex', alignItems: 'center', justifyContent: 'center', bgcolor: '#f5f5f5', p: 3, textAlign: 'center' }}
                >
                  <Box>
                    <Typography variant="h6" color="textSecondary" gutterBottom>
                        Gráfico Indisponível
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                        {dadosFiltrados.length > 200 
                        ? "Muitos dados para exibir no gráfico. Filtre por um ativo específico." 
                        : "Nenhum dado encontrado."}
                    </Typography>
                  </Box>
                </Paper>
              )}
            </Box>
          </Box>
        </Paper>
      </Box>
    </Box>
  );
}

export default DashboardAtivos;