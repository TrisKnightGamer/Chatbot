import React, {Component} from 'react';
import Message from "../Message";
import './style.css'

export default class MessageList extends Component {

    constructor(props) {
        super(props)
        this.state = {
            msgList: null
        }
    }

   scrollToBottom = () => {
       this
           .messagesEnd
           .scrollIntoView();
  }
    
    async componentDidUpdate() {
        setTimeout(()=>{
            console.log("Waiting for render message") 
        }, 750)
        const res = await fetch('http://58.187.249.160:5000/api/v1/messages');
        const data = await res.json()
        this.setState({msgList: data.results})
        //this.scrollToBottom();
    }
    async componentDidMount() {
        const res = await fetch('http://58.187.249.160:5000/api/v1/messages');
        const data = await res.json()
        console.log(data)
        this.setState({msgList: data.results})
        this.scrollToBottom();
    }

    render() {
        return (
            <div className="MessageContainer">
                <div className="MessageList">
                    {this.state.msgList
                        ? this
                            .state
                            .msgList
                            .map((e, idx) => {
                                const align = (e.isBot === true)
                                    ? 'left'
                                    : 'right'
                                return (<Message key={idx} isBot={e.isBot} align={align} content={e.content}/>)
                            })
                        : null
}
                    <div
                        style={{
                        float: "left",
                        clear: "both"
                    }}
                        ref={(el) => {
                        this.messagesEnd = el;
                    }}></div>
                </div>

            </div>

        );
    }

}
// 0,Xin chào bot,hello
// 1,Chào,hello
// 2,Hello,hello
// 3,Hế lô,hello
// 4,Chào bạn,hello
// 5,hey bot, giúp với,hello
// 6,xin chào, giúp tui với,hello
// 7,Hello bot,hello
// 8,xin chào bạn,hello
// 9,xin chào bot,hello
// 10,Chào bot, ngày mới tốt lành,hello
// 11,Chào buổi sáng,hello
// 12,Chào buổi chiều,hello
// 13,Chào buổi tối,hello
// 14,hello,hello
// 15,hi bot,hello
// 16,nè bot ,hello
// 17,Hi,hello
// 18,bot ơi tui hỏi cái này tí,hello
// 19,bot ơi tui có cái này muốn hỏi,hello
// 20,bot ơi,hello
// 21,aloooo,hello
// 22,aloo bot,hello
// 23,alooo bot ơi,hello
// 24,bot đâu,hello
// 25,bot ơi,hello
// 26,bot đâu rồi ,hello
// 0,giới_thiệu đi bot,introduction
// 1,giới_thiệu,introduction
// 2,bot vây,introduction
// 3,khả_năng mày,introduction
// 4,khả_năng,introduction
// 5,khả_năng,introduction
// 6,giới_thiệu đi,introduction
// 7,giới_thiệu,introduction
// 8,khả_năng,introduction
// 9,kỹ_năng,introduction
// 10,bot khả_năng,introduction
// 11,who are you,introduction
// 12,bot là gì vậy,introduction
// 13,bot là ai,introduction
// 14,bot là cái gì_vậy,introduction
// 15,bạn là ai ,introduction
// 16,bạn là gì,introduction
// 17,hãy giới thiệu về bot đi,introduction