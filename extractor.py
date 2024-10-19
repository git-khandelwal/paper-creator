# To be replaced with LangChain outputs
async def gemini_extraction(file):
    return {
  "title": "Sample Maths Paper",
  "type": "Mock",
  "time": 180,
  "marks": 360,
  "params": {
    "board": "CBSE",
    "grade": 12,
    "subject": "Maths"
  },
  "tags": [
    "Calculus", "Geometry"
  ],
  "chapters": [
    "Calculus", "Geometry"
  ],
  "sections": [
    {
      "marks_per_question": 5,
      "type": "default",
      "questions": [
         {
 "question": "Solve the quadratic equation: x^2 + 5x + 6 = 0",
 "answer": "The solutions are x = -2 and x = -3",
 "type": "short",
 "question_slug": "solve-quadratic-equation",
 "reference_id": "QE001",
 "hint": "Use the quadratic formula or factorization method",
 "params": {}
 },
 {
 "question": "In a right-angled triangle, if one angle is 30°, what is the other acute angle?",
 "answer": "60°",
 "type": "short",
 "question_slug": "right-angle-triangle-angles",
 "reference_id": "GT001",
 "hint": "Remember that the sum of angles in a triangle is 180°",
 "params": {}
 }
      ]
    }
  ]
} 