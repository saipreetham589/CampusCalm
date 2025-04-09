const express = require('express');
const router = express.Router();
const sql = require('mssql');
const db = require('../db'); // adjust based on how you connect to Azure SQL

// POST /api/result
router.post('/', async (req, res) => {
  const { userID, phq9Score, gad7Score } = req.body;
  const timestamp = new Date();

  try {
    await db.request()
      .input('UserID', sql.Int, userID)
      .input('PHQ9Score', sql.Int, phq9Score)
      .input('GAD7Score', sql.Int, gad7Score)
      .input('Timestamp', sql.DateTime, timestamp)
      .query(`
        INSERT INTO UserResults (UserID, PHQ9Score, GAD7Score, Timestamp)
        VALUES (@UserID, @PHQ9Score, @GAD7Score, @Timestamp)
      `);

    res.status(200).send('Result saved');
  } catch (err) {
    console.error(err);
    res.status(500).send('Error saving result');
  }
});

// GET /api/result/:userID
router.get('/:userID', async (req, res) => {
  const { userID } = req.params;

  try {
    const result = await db.request()
      .input('UserID', sql.Int, userID)
      .query(`
        SELECT TOP 1 PHQ9Score, GAD7Score, Timestamp
        FROM UserResults
        WHERE UserID = @UserID
        ORDER BY Timestamp DESC
      `);

    if (result.recordset.length === 0) {
      return res.status(404).send('No result found');
    }

    res.json(result.recordset[0]);
  } catch (err) {
    console.error(err);
    res.status(500).send('Error fetching result');
  }
});

module.exports = router;
