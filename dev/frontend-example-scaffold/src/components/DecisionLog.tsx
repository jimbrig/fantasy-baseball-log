import React, { useState } from 'react';
import { format } from 'date-fns';
import { PlusCircle, Filter, Calendar, CheckCircle2, AlertCircle } from 'lucide-react';
import type { Decision, DecisionType } from '../types';
import { useQuery } from 'react-query';
import { yahooService } from '../services/yahoo';

const SAMPLE_DECISIONS: Decision[] = [
  {
    id: '1',
    type: 'draft',
    date: '2024-03-15',
    title: 'Drafted Ronald Acuña Jr. - 1st Overall',
    description: 'Selected Acuña with the first pick due to his 40/70 potential and category dominance.',
    impact: 'Expected to provide strong contributions in R, HR, RBI, SB, and AVG.',
    categories: ['R', 'HR', 'RBI', 'SB', 'AVG']
  },
  {
    id: '2',
    type: 'waiver',
    date: '2024-03-16',
    title: 'Added Jarren Duran - Dropped Luke Raley',
    description: 'Duran showing improved contact rates and regular playing time.',
    impact: 'Looking to improve team speed and AVG without sacrificing power.',
    result: 'Positive - Duran went 3/4 with 2 SB in first start',
    categories: ['SB', 'AVG', 'R']
  }
];

const DecisionLog: React.FC = () => {
  const [decisions] = useState<Decision[]>(SAMPLE_DECISIONS);
  const [selectedType, setSelectedType] = useState<DecisionType | 'all'>('all');

  const { data: transactions } = useQuery('transactions', () => yahooService.getTransactions(), {
    onSuccess: (data) => {
      console.log('Transactions:', data);
    },
  });

  const filteredDecisions = selectedType === 'all' 
    ? decisions 
    : decisions.filter(d => d.type === selectedType);

  const getTypeColor = (type: DecisionType): string => {
    const colors = {
      draft: 'bg-blue-100 text-blue-800',
      waiver: 'bg-green-100 text-green-800',
      trade: 'bg-purple-100 text-purple-800',
      lineup: 'bg-yellow-100 text-yellow-800',
      general: 'bg-gray-100 text-gray-800'
    };
    return colors[type];
  };

  return (
    <div className="max-w-5xl mx-auto p-6">
      <div className="flex justify-between items-center mb-8">
        <h2 className="text-2xl font-bold text-gray-900">Decision Log</h2>
        <button className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
          <PlusCircle className="w-5 h-5 mr-2" />
          New Decision
        </button>
      </div>

      <div className="flex items-center gap-4 mb-6">
        <div className="flex items-center bg-gray-100 rounded-lg p-2">
          <Filter className="w-5 h-5 text-gray-500 mr-2" />
          <select 
            className="bg-transparent border-none focus:ring-0 text-gray-700"
            value={selectedType}
            onChange={(e) => setSelectedType(e.target.value as DecisionType | 'all')}
          >
            <option value="all">All Types</option>
            <option value="draft">Draft</option>
            <option value="waiver">Waiver</option>
            <option value="trade">Trade</option>
            <option value="lineup">Lineup</option>
            <option value="general">General</option>
          </select>
        </div>
      </div>

      <div className="space-y-4">
        {filteredDecisions.map((decision) => (
          <div key={decision.id} className="bg-white rounded-lg shadow-sm border p-6">
            <div className="flex items-start justify-between">
              <div className="flex items-center gap-3">
                <span className={`px-3 py-1 rounded-full text-sm font-medium ${getTypeColor(decision.type)}`}>
                  {decision.type.charAt(0).toUpperCase() + decision.type.slice(1)}
                </span>
                <div className="flex items-center text-gray-500">
                  <Calendar className="w-4 h-4 mr-1" />
                  {format(new Date(decision.date), 'MMM d, yyyy')}
                </div>
              </div>
              {decision.result && (
                <span className="flex items-center text-sm">
                  {decision.result.toLowerCase().includes('positive') ? (
                    <CheckCircle2 className="w-4 h-4 text-green-500 mr-1" />
                  ) : (
                    <AlertCircle className="w-4 h-4 text-red-500 mr-1" />
                  )}
                  {decision.result}
                </span>
              )}
            </div>
            
            <h3 className="text-lg font-semibold mt-3 text-gray-900">{decision.title}</h3>
            <p className="mt-2 text-gray-600">{decision.description}</p>
            
            <div className="mt-4">
              <h4 className="text-sm font-medium text-gray-700">Expected Impact:</h4>
              <p className="mt-1 text-gray-600">{decision.impact}</p>
            </div>

            {decision.categories && (
              <div className="mt-4 flex flex-wrap gap-2">
                {decision.categories.map((category) => (
                  <span 
                    key={category}
                    className="px-2 py-1 bg-gray-100 text-gray-700 rounded-md text-sm"
                  >
                    {category}
                  </span>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default DecisionLog;