module SocketIO = {
    type t;
    [@bs.new] external create : unit => t = "io";
    [@bs.new] external createWithUrl : string => t = "io";
    [@bs.send] external _emit : (t, string, 'a) => unit = "emit";
    let emit = (socket, tag, obj: string) =>
      _emit(socket, tag, obj);
    [@bs.send] external _on : (t, string, string => unit) => unit = "on";
    let onStatus = (socket, func: Messages.status => unit) =>
      _on(socket, "status", obj => {                    
            func(Messages.parse_status(obj))
            }
        );
  };

let socket = SocketIO.createWithUrl("http://localhost:8000/");

Random.init(int_of_float(Js.Date.now()));

type state = {
    current: string,
    items: list(Messages.status)
};

type action =
    | Enter
    | Text(string)
    | Update(Messages.status);

let component = ReasonReact.reducerComponent("Translator");

let make = (_children) => {
    ...component, 
    
    initialState: () => {items: [], current: ""}, 
    
    didMount: self => {
        SocketIO.onStatus(socket, (status: Messages.status) => {            
            self.send(Update(status));
            }   
        );        
    },

    reducer: ((action: action), (state: state)) => {        
        let exists = (text: string) : bool => 
            List.exists( (i: Messages.status) => i.text == text, state.items);
        switch (action) {
        | Enter =>                  
            Js.log("ENTER");
            let text = state.current;                        
            switch (exists(text)) {
            | true =>
                ReasonReact.NoUpdate;                            
            | false =>
                let event: Messages.translate_event = {text: text};
                let new_item : Messages.status = {uid: 0, text: text, translation: "", status: "Sent"};
                let new_state = {current: "", items: [new_item,  ...state.items]};                                
                ReasonReact.UpdateWithSideEffects(new_state, _self =>
                    SocketIO.emit(socket, "translate", Messages.encode_event(event))
                )
            }
        | Text(content) =>            
            ReasonReact.Update({...state, current: content})

        | Update(status) =>
            switch (exists(status.text))  {
            | true => 
                let new_items = List.map( (i: Messages.status) => {
                    switch (i.text == status.text) {
                    | true => {...i, uid: status.uid, translation: status.translation, status: status.status}
                    | false => i
                    }
                }, state.items );
                ReasonReact.Update({...state, items: new_items});
            | false =>
                ReasonReact.NoUpdate;    
            }            
        }
    },
    render: self => {
        <div>
            <form>
                <div className="form-group">            
                    <textarea
                        className="form-control"
                        id="input"                         
                        onChange = ( (event) => {
                            let content = ReactEvent.Form.target(event)##value;
                            self.send(Text(content)) })
                        onKeyDown = ((event) => 
                            switch (ReactEvent.Keyboard.key(event) == "Enter") {
                            | true => 
                                /* ReactEvent.Keyboard.preventDefault(event);  */
                                self.send(Enter)
                            | false => 
                                ()                                
                            }
                        )
                        /> 
                </div>            
            </form>            
            <ul className="list-group list-group-flush">
            { ReasonReact.array(
            self.state.items 
            |> List.map( (item: Messages.status) => 
                <li className="list-group-item d-flex justify-content-between align-items-center" key={item.text}>
                <p className="mb-1">{ReasonReact.string(item.text)}</p>
                <p className="mb-1">{ReasonReact.string(item.translation)}</p>
                <span className="badge badge-primary badge-pill">{
                    {ReasonReact.string(item.status)}
                }</span>
                </li>
                )  
            |> Array.of_list
            )}
            </ul>            
        </div>
        
    }
};


