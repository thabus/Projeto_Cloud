import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from "recharts";
import { Paper, Typography } from "@mui/material";

function GraficoAcoes({ dados }) {
  return (
    <Paper sx={{ p: 2, width: 350, height: 320, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center" }}>
      <Typography variant="subtitle1">Fechamento por data</Typography>
      <ResponsiveContainer width="95%" height={250}>
        <LineChart data={dados}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="trade_date" />
          <YAxis />
          <Tooltip />
          <Line type="monotone" dataKey="close_price" stroke="#2566cf" />
        </LineChart>
      </ResponsiveContainer>
    </Paper>
  );
}

export default GraficoAcoes;