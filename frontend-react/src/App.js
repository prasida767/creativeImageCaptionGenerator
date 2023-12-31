import React, { useState } from 'react';
import Header from './Components/Header/Header';
import MainContent from './Components/main/MainContent';
import Footer from './Components/Footer/Footer';
import './App.css'
import { BrowserRouter, Routes, Route} from 'react-router-dom';
import ErrorPage from './Components/ErrorPage/ErrorPage';
import Train from './Components/Train/Train';
import Test from './Components/Test/Test';


const App = () => {
  const title = "Creative Image Caption Generator";
  const train = "Train Your Model";
  const test = "Test Your Model";

  return (
    <div className="main-app">

      <Header title={title} train={train} test={test}/>
      
      <Routes>
      <Route path="/" element ={<MainContent/>} />
      <Route path="train" element= {<Train/>}/>
      <Route path="test" element= {<Test/>}/>
      <Route path="*" element={<ErrorPage />} />
      </Routes>
      <Footer note = "Copyright © 2023 Birkbeck, University of London. All rights reserved."/>

    
      
    </div>
  );
};

export default App;