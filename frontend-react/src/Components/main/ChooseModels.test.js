import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import ChooseModels from './ChooseModels';

describe('ChooseModels component', () => {
  // Mock the data for the trained models and their performance data
  const trainedModels = {
    'Model 1': ['Architecture 1', 'Architecture 2'],
    'Model 2': ['Architecture 3', 'Architecture 4'],
  };

  const modelsPerformance = {
    'Architecture 1___Model 1___Epochs___uniqueKey': [/* performance data */],
  };

  // Mock callback functions
  const onModelChange = jest.fn();
  const onArchitectureChange = jest.fn();
  const onPerformanceClick = jest.fn();

  beforeEach(() => {
    render(
      <ChooseModels
        trainedModels={trainedModels}
        modelsPerformance={modelsPerformance}
        selectedModel="Model1"
        selectedArchitecture="Architecture1"
        onModelChange={onModelChange}
        onArchitectureChange={onArchitectureChange}
        onPerformanceClick={onPerformanceClick}
      />
    );
  });

  it('renders the component with initial state', () => {
    // Ensure that the component renders the initial options and labels
    expect(screen.getByText('Choose your Models')).toBeInTheDocument();
    expect(screen.getByLabelText('Available Models:')).toBeInTheDocument();
  });

  it('handles model selection and architecture selection', async () => {
    // Simulate selecting a model
    fireEvent.change(screen.getByLabelText('Available Models:'), {
      target: { value: 'Model 1' },
    });

    // Ensure the onModelChange function is called with the selected model
    expect(onModelChange).toHaveBeenCalledWith(trainedModels['Model 1']);

    // Simulate selecting an architecture
    fireEvent.change(screen.getByLabelText('Version of Model 1:'), {
      target: { value: 'Architecture 1' },
    });

    // Ensure the onArchitectureChange function is called with the selected architecture
    expect(onArchitectureChange).toHaveBeenCalledWith('Architecture 1');
  });

//   it('handles performance click and displays the chart modal', async () => {
//     // Simulate selecting a model and architecture
//     fireEvent.change(screen.getByLabelText('Available Models:'), {
//       target: { value: 'Model 1' },
//     });
//     fireEvent.change(screen.getByLabelText('Version of Model 1:'), {
//       target: { value: 'Architecture 1' },
//     });

//     // Simulate clicking the "See Model's Performance" button
//     fireEvent.click(screen.getByText("See Model's Performance"));

//     // Ensure the onPerformanceClick function is called with the expected data
//     expect(onPerformanceClick).toHaveBeenCalledWith(modelsPerformance['Architecture 1___Model 1___Epochs___uniqueKey']);

//     // Ensure the chart modal is displayed
//     expect(screen.getByText('Model Performance')).toBeInTheDocument();
//     expect(screen.getByText('Close')).toBeInTheDocument();
//   });

  // Additional tests...
});