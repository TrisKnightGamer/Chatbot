import React, {Component} from 'react';
import useLongPress from "./useLongPress";
import {TextField} from "@material-ui/core";
import SpeechRecognition, { useSpeechRecognition } from 'react-speech-recognition'
// import Icon  from "@material-ui/icons";
import './style.css'

// eslint-disable-next-line
function Hook(Component) {
    return function WrappedComponent(props) {
        const transcript = useSpeechRecognition()
        const resetTranscript = useSpeechRecognition()
        const onLongPress = () => {
            SpeechRecognition.startListening({continuous: true });
        };

        const onClick = () => {
            console.log('click is triggered')
        }

        const defaultOptions = {
            shouldPreventDefault: true,
            delay: 500,
        };
        const longPressEvent = useLongPress(onLongPress, onClick, defaultOptions);
        return <Component {...props} transcript={transcript} resetTranscript={resetTranscript} longPress = {longPressEvent}/>;
        
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
            fetch('https://34.247.120.53:5000/api/v1/messages', {
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
                            
                            fetch('https://34.247.120.53:5000/api/v1/messages/reply', {
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
        SpeechRecognition.stopListening();
        this.state.message = this.props.transcript;
        if (this.state.message !== this.props.transcript) {
            return
        } else {
            fetch('https://34.247.120.53:5000/api/v1/messages', {
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
                            
                            fetch('https://34.247.120.53:5000/api/v1/messages/reply', {
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
                                    console.log("Wait for reply ...");
                                    this.props.resetTranscript();
                                } else {
                                    console.log("Some error occured");
                                    this.props.resetTranscript();
                                }
                            })
                        })
                    this.state.message = this.props.resetTranscript();

                } else {
                    console.log("Some error occured");
                    this.props.resetTranscript();
                }
            }).then(this.setState({message: ""}))
            this.props.resetTranscript();
        }
    }

    render() {

        if (!SpeechRecognition.browserSupportsSpeechRecognition()) {
            alert("Browser don't support Speech Recognation. If you want to use this feature please use following browsers : Microsoft Edge, Chrome, Android webview, Samsung Internet");
        }
        return (
            <div className="SendMessageForm">
                <div className="chat-input-width-100">
                    <form className="MessageForm" onKeyUp={this.handleEnter}>
                        <button className="sender" type="button" onClick={(e) => this.handleSubmit(e)}>
                            <img src="send.png" alt=""/>
                        </button> 
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
                            <img src="voice.png" alt="button" {...this.props.longPress} onTouchEnd={this.handleButtonRelease} onMouseUp={this.handleButtonRelease} onMouseLeave={this.handleButtonRelease} style={{height:30+'px', width:30+'px', marginTop:15+'px'}}/>
                    </form>
                </div>
            </div>
        )
    }
}

