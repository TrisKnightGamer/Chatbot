import React, {Component} from 'react'
import {TextField} from "@material-ui/core";
import SpeechRecognition, { useSpeechRecognition } from 'react-speech-recognition'
// import Icon  from "@material-ui/icons";
import './style.css'

// eslint-disable-next-line
function Hook(Component) {
    return function WrappedComponent(props) {
      const transcript = useSpeechRecognition()
      const resetTranscript = useSpeechRecognition()
      return <Component {...props} transcript={transcript} resetTranscript={resetTranscript} />;
    }
}



export default class SendMessageForm extends Component  {
    constructor(props) {
        super();
        this.state = {
            message: "",
            alert:true
        }
        this.handleEnter = this
            .handleEnter
            .bind(this)
        this.handleSubmit = this
            .handleSubmit
            .bind(this)
        this.onChange = this
            .onChange
            .bind(this)
        this.handleButtonPress = this
            .handleButtonPress
            .bind(this)
        this.handleButtonRelease = this
            .handleButtonRelease
            .bind(this)
    }
    async handleSubmit(e) {
        e.preventDefault()
        await this.setState({
            message: this
                .state
                .message
                .replace(/(\r\n|\n|\r)/gm, "")
        })

        if (this.state.message === "") {
            return
        } else {
            fetch('http://0.0.0.0:5000/api/v1/messages', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    Accept: 'application/json'
                },
                body: JSON.stringify({
                    content: this.state.message,
                    isBot: false,
                    time: (new Date().getTime()) / 1000
                })
            }).then(res => {
                if (res.status === 200) {
                    console.log("Send message successfully")
                    res
                        .json()
                        .then(postResponse => {
                            console.log(postResponse);
                            
                            fetch('http://0.0.0.0:5000/api/v1/messages/reply', {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/json',
                                    Accept: 'application/json'
                                },
                                body: JSON.stringify({
                                    content: postResponse.content,
                                    isBot: false,
                                    time: (new Date().getTime()) / 1000
                                })
                            }).then(res => {
                                if (res.status === 200) {
                                    console.log("Wait for reply ...")
                                } else {
                                    console.log("Some error occured");

                                }
                            })
                        })

                } else {
                    console.log("Some error occured");
                }
            }).then(this.setState({message: ""}))

        }

    }
    handleEnter(e) {
        if (e.keyCode === 13) {
            return this.handleSubmit(e)
        }
        return
    }
    onChange(e) {
        this.setState({
            [e.target.name]: e.target.value
        });
    }
    handleButtonPress () {
        let buttonPressTimer
        if(this.state.alert){
            buttonPressTimer = setTimeout(() => SpeechRecognition.startListening({continuous: true }), 200);
        }
        else{
            clearTimeout(buttonPressTimer);
        }
    }
    
    async handleButtonRelease () {

        if (this.state.message === "") {
            return
        } else {
            fetch('http://0.0.0.0:5000/api/v1/messages', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    Accept: 'application/json'
                },
                body: JSON.stringify({
                    content: this.state.message,
                    isBot: false,
                    time: (new Date().getTime()) / 1000
                })
            }).then(res => {
                if (res.status === 200) {
                    console.log("Send message successfully")
                    res
                        .json()
                        .then(postResponse => {
                            console.log(postResponse);
                            
                            fetch('http://0.0.0.0:5000/api/v1/messages/reply', {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/json',
                                    Accept: 'application/json'
                                },
                                body: JSON.stringify({
                                    content: postResponse.content,
                                    isBot: false,
                                    time: (new Date().getTime()) / 1000
                                })
                            }).then(res => {
                                if (res.status === 200) {
                                    console.log("Wait for reply ...")
                                } else {
                                    console.log("Some error occured");

                                }
                            })
                        })

                } else {
                    console.log("Some error occured");
                }
            }).then(this.setState({message: ""}))

        }
    }

    render() {
        if (!SpeechRecognition.browserSupportsSpeechRecognition()) {
            return null
        }
        return (
            <div className="SendMessageForm">
                <div className="chat-input-width-100">
                    <form className="MessageForm" onKeyUp={this.handleEnter}>
                        <TextField
                            name="message"
                            id="outlined-multiline-static"
                            fullWidth={false}
                            multiline
                            rows="4"
                            value={this.state.message}
                            placeholder="Type something here"
                            className="chat-input"
                            style={{
                                width:"925px"
                            }}
                            margin="normal"
                            variant="outlined"
                            onChange={this.onChange}/>
                        <img src="send.png" alt="button" onMouseDown={(e) => this.handleSubmit(e)} style={{height:30+'px', width:30+'px', marginTop:15+'px'}}/>   
                        <img src="voice.png" alt="button" onTouchStart={this.handleButtonPress} 
                                onTouchEnd={SpeechRecognition.stopListening, this.state.message = this.props.transcript, this.handleButtonRelease} 
                                onMouseDown={this.handleButtonPress} 
                                onMouseUp={SpeechRecognition.stopListening, this.state.message = this.props.transcript, this.handleButtonRelease} 
                                onMouseLeave={SpeechRecognition.stopListening, this.state.message = this.props.transcript, this.handleButtonRelease} style={{height:30+'px', width:30+'px', marginTop:15+'px'}}/>
                        <p hidden>
                            {setInterval(this.props.resetTranscript,4000)}
                        </p>
                    </form>
                </div>
            </div>
        )
    }
}

