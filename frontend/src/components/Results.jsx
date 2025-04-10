// Results.jsx
import React from 'react';

const Results = ({ data }) => {
  if (!data) return null;

  return (
    <div className="p-4 border rounded mt-4">
      <h2 className="text-xl font-semibold mb-2">Results</h2>
      <p className="mb-2"><strong>Resume Match Score:</strong> {data['Resume Match Score']}</p>
      <div>
        <h3 className="font-semibold">Extracted Information:</h3>
        <pre className="bg-gray-100 p-2 rounded mt-1 text-sm">
          {JSON.stringify(data['Extracted Information'], null, 2)}
        </pre>
      </div>
    </div>
  );
};

export default Results;
