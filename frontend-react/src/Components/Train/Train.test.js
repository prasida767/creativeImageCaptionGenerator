// import React from 'react';
// import { render, screen, fireEvent, waitFor } from '@testing-library/react';
// import Train from './Train';

// describe('Train component', () => {
//   it('renders the component with initial state', () => {
//     render(<Train />);
    
//     // Test that various elements are rendered
//     expect(screen.getByText('Train Model')).toBeInTheDocument();
//     expect(screen.getByLabelText('Dataset:')).toBeInTheDocument();
//     expect(screen.getByLabelText('No. of Training Parameters:')).toBeInTheDocument();
//     // Add more assertions for other form elements and labels as needed
//   });

//   it('handles form input changes and validation', async () => {
//     render(<Train />);
    
//     // Simulate input changes and validate error messages
//     fireEvent.change(screen.getByLabelText('No. of Training Parameters:'), { target: { value: 'abc' } });
//     fireEvent.blur(screen.getByLabelText('No. of Training Parameters:'));
    
//     await waitFor(() => {
//       expect(screen.getByText('Must be an integer value between 1000 and 8000')).toBeInTheDocument();
//     });

//     // Add more input changes and validation tests as needed
//   });

//   it('handles the "Train Model" button click and API call', async () => {
//     // Mock the fetch function to simulate API response
//     global.fetch = jest.fn(() =>
//       Promise.resolve({
//         json: () =>
//           Promise.resolve({
//             parameters: {
//               model_summary: 'Mock model summary',
//               // Add other mock data as needed
//             },
//           }),
//       })
//     );

//     render(<Train />);
    
//     // Simulate form input changes
//     fireEvent.change(screen.getByLabelText('Dataset:'), { target: { value: 'Flickr8k' } });
//     fireEvent.change(screen.getByLabelText('No. of Training Parameters:'), { target: { value: '2000' } });
//     // Add more input changes as needed
    
//     // Simulate "Train Model" button click
//     fireEvent.click(screen.getByText('Train Model'));

//     // Wait for the API call to complete
//     await waitFor(() => {
//       expect(screen.getByText('Mock model summary')).toBeInTheDocument();
//       // Add assertions for other API response data as needed
//     });

//     // Verify that the fetch function was called with the expected URL and data
//     expect(global.fetch).toHaveBeenCalledWith('http://127.0.0.1:8000/train_models/train/', {
//       method: 'POST',
//       headers: {
//         'Content-Type': 'application/json',
//       },
//       body: JSON.stringify({
//         dataset: 'Flickr8k',
//         trainingParams: '2000',
//         // Add other expected data here
//       }),
//     });
//   });
// });