import logo from './logo.svg';
import './App.css';
import Button from 'react-bootstrap/Button'
import Container from 'react-bootstrap/Container'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'
import Form from 'react-bootstrap/Form'
import FormControl from 'react-bootstrap/FormControl'
import SearchResults from './components/searchResults/SearchResults';
import { useRef } from 'react';
import { useState } from 'react';
import Navbar from 'react-bootstrap/Navbar'
import homepageImage from './homepage.png'

function App() {

  const fref = useRef()
  const [queryTxt, setQueryTxt] = useState("");


  const searchIfEnter = (e) => {
    if (e.key === "Enter") {
      search();
    }
  }


  const reset = () => {
    setQueryTxt("")
    fref.current.reset();
  }

  const search = () => {
    if (queryTxt.trim().length > 0) {
      fref.current.search(queryTxt)
    }
  }

  return (
    <Container id="parentContainer" fluid>
      <Container id="navContainer" fluid>
        <Navbar expand="lg" className = "navbar-custom" sticky="top">
          <Container id="bannerContainer" fluid>
            <Navbar.Brand href="#" id="title"><img
              src={homepageImage}
              width="120"
              height="50"
            /><span id="titleSpan">Smart Video Search</span></Navbar.Brand>
          </Container>
        </Navbar>
      </Container>

      <Container id="contentContainer">
        <Row>
          <Col>
            <Form>
              <Row className="justify-content-md-center">
                <Col sm={{ span: 8, offset: 1 }}>
                  <Form.Label htmlFor="inlineFormInput" visuallyHidden> Name </Form.Label>
                  <Form.Control className="mb-2" id="inlineFormInput" placeholder="Enter the query" value={queryTxt} onKeyPress={e => searchIfEnter(e)} onChange={e => setQueryTxt(e.target.value)} />
                </Col>
                <Col>
                  <Button id="srchBtn" variant="primary" onClick={search}>
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-search" viewBox="0 0 16 16">
                      <path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0z" />
                    </svg>Search </Button>
                </Col>
                <Col>
                  <Button variant="warning" onClick={reset}> Reset </Button>
                </Col>
              </Row>
              <Row>
                <hr></hr>
              </Row>
            </Form>
          </Col>
        </Row>
        <Row>
          <SearchResults ref={fref}></SearchResults>
        </Row>
      </Container>
    </Container>
  );
}

export default App;
