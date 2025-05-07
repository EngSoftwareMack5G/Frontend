const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const cors = require('cors');
const bodyParser = require('body-parser');

const app = express();
const port = 3000;

app.use(cors());
app.use(bodyParser.json());

// Banco de dados SQLite
const db = new sqlite3.Database('./mentorias.db');

// Cria as tabelas se não existirem
db.serialize(() => {
    db.run(`CREATE TABLE IF NOT EXISTS perfis (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT
    )`);

    db.run(`CREATE TABLE IF NOT EXISTS mentorias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT,
        descricao TEXT,
        autor TEXT,
        data TEXT,
        topico TEXT,
        inscritos INTEGER DEFAULT 0
    )`);

    // Preenche perfis de exemplo se estiver vazio
    db.all(`SELECT * FROM perfis`, [], (err, rows) => {
        if (rows.length === 0) {
            const perfis = ['João', 'Maria', 'Carlos', 'Ana'];
            perfis.forEach(nome => {
                db.run(`INSERT INTO perfis (nome) VALUES (?)`, [nome]);
            });
        }
    });
});

// Rota: lista todos os perfis
app.get('/perfis', (req, res) => {
    db.all(`SELECT * FROM perfis`, [], (err, rows) => {
        if (err) return res.status(500).json({ error: err.message });
        res.json(rows);
    });
});

// Rota: lista todas as mentorias
app.get('/mentorias', (req, res) => {
    db.all(`SELECT * FROM mentorias`, [], (err, rows) => {
        if (err) return res.status(500).json({ error: err.message });
        res.json(rows);
    });
});

// Rota: adiciona uma nova mentoria
app.post('/mentorias', (req, res) => {
    const { titulo, descricao, autor, data, topico } = req.body;
    db.run(`INSERT INTO mentorias (titulo, descricao, autor, data, topico) VALUES (?, ?, ?, ?, ?)`,
        [titulo, descricao, autor, data, topico],
        function(err) {
            if (err) return res.status(500).json({ error: err.message });
            res.json({ id: this.lastID });
        });
});

// Rota: edita uma mentoria
app.put('/mentorias/:id', (req, res) => {
    const id = req.params.id;
    const { titulo, descricao, data, topico } = req.body;
    db.run(`UPDATE mentorias SET titulo = ?, descricao = ?, data = ?, topico = ? WHERE id = ?`,
        [titulo, descricao, data, topico, id],
        function(err) {
            if (err) return res.status(500).json({ error: err.message });
            res.json({ changes: this.changes });
        });
});

// Rota: deleta uma mentoria
app.delete('/mentorias/:id', (req, res) => {
    const id = req.params.id;
    db.run(`DELETE FROM mentorias WHERE id = ?`, [id], function(err) {
        if (err) return res.status(500).json({ error: err.message });
        res.json({ changes: this.changes });
    });
});

// Inicia o servidor
app.listen(port, () => {
    console.log(`Servidor rodando em http://localhost:${port}`);
});
