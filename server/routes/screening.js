const express = require('express');
const router = express.Router();
const { sql, pool } = require('../db');

// GET /api/questions - Fetch all questions
router.get('/questions', async (req, res) => {
  try {
    const result = await pool.request().query(`
      SELECT QuestionID, QuestionText
      FROM dbo.Questions
      ORDER BY QuestionID
    `);
    res.json(result.recordset);
  } catch (err) {
    console.error('Error fetching questions:', err);
    res.status(500).json({ error: 'Failed to fetch questions' });
  }
});

// GET /api/responses - Fetch responses grouped by QuestionID
router.get('/responses', async (req, res) => {
  try {
    const result = await pool.request().query(`
      SELECT QuestionID, OptionText, OptionValue
      FROM dbo.Responses
      ORDER BY QuestionID, OptionValue
    `);
    const grouped = result.recordset.reduce((acc, row) => {
      acc[row.QuestionID] = acc[row.QuestionID] || [];
      acc[row.QuestionID].push({ text: row.OptionText, value: row.OptionValue });
      return acc;
    }, {});
    res.json(grouped);
  } catch (err) {
    res.status(500).json({ error: 'Failed to fetch responses' });
  }
});

// POST /api/answers - Save an answer
router.post('/answers', async (req, res) => {
    const { userID, questionID, selectedValue } = req.body;
    try {
      await pool.request()
        .input('UserID', sql.Int, userID)
        .input('QuestionID', sql.Int, questionID)
        .input('SelectedValue', sql.Int, selectedValue)
        .query(`
          INSERT INTO dbo.UserAnswers (UserID, QuestionID, SelectedValue, AnsweredAt)
          VALUES (@UserID, @QuestionID, @SelectedValue, GETDATE())
        `);
      res.json({ success: true });
    } catch (err) {
      console.error('Error saving answer:', err);
      res.status(500).json({ error: 'Failed to save answer' });
    }
  });

// POST /api/result - Save total result
router.post('/result', async (req, res) => {
    const { userID, totalScore, difficultyLevel } = req.body;
    try {
      await pool.request()
        .input('UserID', sql.Int, userID)
        .input('TotalScore', sql.Int, totalScore)
        .input('DifficultyLevel', sql.NVarChar, difficultyLevel)
        .query(`
          INSERT INTO dbo.UserResults (UserID, TotalScore, DifficultyLevel, SubmittedAt)
          VALUES (@UserID, @TotalScore, @DifficultyLevel, GETDATE())
        `);
      res.json({ success: true });
    } catch (err) {
      console.error('Error saving result:', err);
      res.status(500).json({ error: 'Failed to save result' });
    }
  });

// GET /api/last-result/:userID - Check if last test was more than 7 days ago
router.get('/last-result/:userID', async (req, res) => {
    const { userID } = req.params;
  
    try {
      const result = await pool.request()
        .input('userID', sql.Int, userID)
        .query(`
          SELECT TOP 1 SubmittedAt
          FROM dbo.UserResults
          WHERE UserID = @userID
          ORDER BY SubmittedAt DESC
        `);
  
      const last = result.recordset[0]?.SubmittedAt;
      const needsTest = !last || new Date() - new Date(last) > 7 * 24 * 60 * 60 * 1000;
  
      res.json({ lastSubmission: last, needsTest });
    } catch (err) {
      console.error('Error fetching last result:', err);
      res.status(500).json({ error: 'Failed to fetch last result' });
    }
  });

module.exports = router;
