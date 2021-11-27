import React from "react";
import { Col, Row } from "react-bootstrap";
import Container from "react-bootstrap/esm/Container";
import Table from "react-bootstrap/Table"
import { Badge } from "react-bootstrap";
import { Image } from "react-bootstrap";
import { Card } from "react-bootstrap";
import CardHeader from "react-bootstrap/esm/CardHeader";

class SearchResults extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            results: [],
            uniqueCourses: new Set()
        }
    }

    reset() {
        this.setState({
            results: [],
            uniqueCourses: new Set()
        })
        delete this.state.emptyResults
    }

    search(queryStr) {

        fetch("http://127.0.0.1:5000/search?q=" + queryStr).then(res => res.json()).then(res => {
            var emptyResults = res.length < 1
            var uniqueCourses = new Set()
            var uniqueCoursesArr;

            res.forEach(s => {
                uniqueCourses.add(s.course)
            });

            if (uniqueCourses.size > 0) {
                uniqueCoursesArr = [...uniqueCourses]
                uniqueCoursesArr.unshift("All")
            }
            this.setState({ results: res, emptyResults: emptyResults, uniqueCourses: uniqueCoursesArr })
        }, (error) => { alert(" error while fetching..") })
    }

    render() {
        return (
            <Container>
                <Row>
                    <tr>
                        <Col id="filterDiv">
                            {
                                // Array.from(this.state.uniqueCourses).map((course, i) => {
                                //     return <td className="filterItem"> <a href="#"><h6><Badge pill bg="dark">{course}</Badge></h6></a> </td>
                                // })
                            }
                        </Col>
                    </tr>
                </Row>
                <br></br>
                <Row>
                    <Col md={12}>
                        <Container id="resultsContainer" fluid>
                            {this.state.results.length > 0 ?
                                <><p id="resCnt" class="text-end">{this.state.results.length} results found</p>
                                    <Row xs={1} md={6}>
                                    {this.state.results.map((res, i) => {
                                        return <>
                                            <Col md={3}>
                                                <Card className = "baseBlock">
                                                    <CardHeader><h6><Badge pill bg="dark">{res.course}</Badge></h6></CardHeader>
                                                    <Card.Img variant="top" src={`data:image/png;base64,${res.img}`} />
                                                    <Card.Title><b>Week {res.week}.{res.video_id} - {res.video_title}</b></Card.Title>
                                                    <Card.Body>
                                                        <Card.Text>
                                                         <Row>
                                                         {res.text_preview}...
                                                         </Row>
                                                         <Badge pill bg="secondary">{res.course_id}</Badge>
                                                        </Card.Text>
                                                        <a href={res.segment_link} target ="_blank" class="stretched-link"></a>
                                                    </Card.Body>
                                                </Card>
                                            </Col>    </>
                                    })
                                    }</Row></>
                                : this.state.emptyResults ? "No Results found" : null}
                        </Container>
                    </Col>
                </Row>
            </Container>
        );
    }
}

export default SearchResults;