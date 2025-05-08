const express = require('express');
const { Pool } = require('pg');
const app = express();

app.use(express.json());

const pool = new Pool({
  user: 'seu_usuario',
  host: 'localhost',
  database: 'test',
  password: 'sua_senha',
  port: 5432,
});

app.post('/inscrever', async (req, res) => {
  const { nome, email, motivo } = req.body;

  try {
    const result = await pool.query(
      'INSERT INTO mentorias (nome, email, motivo) VALUES ($1, $2, $3) RETURNING *',
      [nome, email, motivo]
    );
    res.status(201).json(result.rows[0]);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Erro ao salvar a inscrição' });
  }
});

app.listen(3000, () => {
  console.log('Servidor rodando na porta 3000');
});