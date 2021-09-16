import React, { Component } from 'react';
import $ from 'jquery';

import '../stylesheets/FormView.css';

class FormView extends Component {
  constructor(props){
    super();
    this.state = {
      question: "",
      answer: "",
      difficulty: 1,
      category: 1,
      categories: []
    }
  }

  componentDidMount(){
    $.ajax({
      url: 'http://localhost:5000/categories', //TODO: update request URL
      type: "GET",
      success: result => {
        console.log("LORENX = ", result.categories)
        this.setState({ categories: result.categories})
        return;
      },
      error: (error) => {
        alert('[FORMVIEW - CATEGO]Unable to load categories. Please try your request again')
        return;
      }
    })
  }


  submitQuestion = (event) => {
    event.preventDefault();
    $.ajax({
      url: 'http://localhost:5000/questions', //TODO: update request URL
      type: "POST",
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({
        question: this.state.question,
        answer: this.state.answer,
        difficulty: this.state.difficulty,
        category: this.state.category
      }),
      xhrFields: {
        withCredentials: true
      },
      crossDomain: true,
      success: result => {
        console.log("TEST = ", result)
        document.getElementById("add-question-form").reset();
        return;
      },
      error: (error) => {
        alert('[FORMVIEW - POST QUESTIONS]Unable to add question. Please try your request again')
        return;
      }
    })
  }

  handleChange = (event) => {
    this.setState({[event.target.name]: event.target.value})
  }

  render() {
  console.log("LORENX 2= ", this.state.categories)
  console.log("LORENX 5= ", Object.keys(this.state.categories))
  Object.keys(this.state.categories).map(id => {
      console.log("LORENX 3 = ", id)
      console.log("LORENX 4 = ", this.state.categories[id])
  })
    return (
      <div id="add-form">
        <h2>Add a New Trivia Question</h2>
        <form className="form-view" id="add-question-form" onSubmit={this.submitQuestion}>
          <label>
            Question
            <input type="text" name="question" onChange={this.handleChange}/>
          </label>
          <label>
            Answer
            <input type="text" name="answer" onChange={this.handleChange}/>
          </label>
          <label>
            Difficulty
            <select name="difficulty" onChange={this.handleChange}>
              <option value="1">1</option>
              <option value="2">2</option>
              <option value="3">3</option>
              <option value="4">4</option>
              <option value="5">5</option>
            </select>
          </label>
          <label>
            Category
            <select name="category" onChange={this.handleChange}>
              {this.state.categories.map(category => {
                  return (
                    <option key={category.id} value={category.id}>{category.type}</option>
                  )
                })}
            </select>
          </label>
          <input type="submit" className="button" value="Submit" />
        </form>
      </div>
    );
  }
}

export default FormView;