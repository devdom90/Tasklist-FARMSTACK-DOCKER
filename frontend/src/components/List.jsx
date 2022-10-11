import React from 'react';
import TaskElement from './TaskElement';
import { useState, useRef, useEffect} from 'react';
import axios from 'axios';




const List = () => {
    const [tasks,setTasks] = useState([]);
    const [token, setToken] = useState("");
    const [loggedIn, setLoggedIn] = useState(false)
    const [loginError, setLoginError] = useState(false)
    const [registerError, setRegisterError] = useState(false)
    const [registerSuccess, setRegisterSuccess] = useState(false)
    const [openTasks, setOpenTasks] = useState(0)

    const usernameRef = useRef();
    const passwordRef = useRef();
    const inputCreateRef = useRef();


    useEffect(() => {
        const countOpenTask = tasks.filter((item) => {
            return !item.done;
        });
        setOpenTasks(countOpenTask.length);
    },[tasks])

    const register = () => {
        axios.post('http://127.0.0.1:8000/register', {
                    username: usernameRef.current.value,
                    password: passwordRef.current.value,
            })
            .then((response) => {
                console.log(response.data);
                setRegisterSuccess(true);
                usernameRef.current.value = "";
                passwordRef.current.value = "";
            })
            .catch((error) => {
                console.log(error);
                setRegisterError(true);
                setTimeout(() => {
                    setregisterError(false);
                  }, 1500);
            });

    };
    const login = () => {
        let data = new FormData()
        data.append("username", usernameRef.current.value)
        data.append("password", passwordRef.current.value)

        axios.post('http://127.0.0.1:8000/login',data)
        .then((response) => {
            setToken(response.data.access_token);
            get_latest_tasks(response.data.access_token);
            setLoggedIn(true);
            usernameRef.current.value = "";
            passwordRef.current.value = "";
        })
        .catch((error) => {
            console.log(error);
            setLoginError(true);
            setTimeout(() => {
                setloginError(false);
              }, 1500);
        })
    };
    const get_latest_tasks = (access_token) => {
        axios.get('http://127.0.0.1:8000/get_all_tasks',{
            headers: {Authorization: `Bearer ${access_token}`}})
        .then((response) => {
            setTasks(response.data);
        })
        .catch((error) => {
            console.log(error);
        })
    };
    const creating_task = () => {
        axios.post('http://127.0.0.1:8000/create_new_task',{
            description: inputCreateRef.current.value,
            done: false,
            },
            {
                headers: {Authorization: `Bearer ${token}`}
            })
        .then(() => {
            get_latest_tasks(token);
            inputCreateRef.current.value = "";
        })
        .catch((error) => {
            console.log(error)
        })
        }
    const delete_task = (id) => {
        axios.delete(`http://127.0.0.1:8000/delete_task_by_user/${id}`,{
            headers: {Authorization: `Bearer ${token}`}
            })
        .then(() => {
            get_latest_tasks(token)
        })
        .catch((error) => {
            console.log(error)
        })
    }
    const update_Task = (id) => {
        axios.put(`http://127.0.0.1:8000/update_task/${id}`,
            {},
            {
            headers: {Authorization: `Bearer ${token}`}
            })
        .then(() => {
            get_latest_tasks(token)
        })
        .catch((error) => {
            console.log(error)
        })
    }

    const logout = (() => {
        setToken("");
        setLoggedIn(false);
    })

  return (
    <>
        <div className='task-wrapper'>
            <h1 className='header-wrapper'>Login / Register</h1>
            <div className='login-input-wrapper'>
                <input type='text' placeholder='Username' ref={usernameRef}/>
                <input type='text' placeholder='Password' ref={passwordRef}/>
            </div>
                <div className='regloginbtns'>
                    <button className='btn'onClick={login}>Login</button>
                    <button className='btn' onClick={register}>Register</button>
                </div>
                    {registerError ? <p className="error-msg">User already exists</p> : ""}
                    {registerSuccess ? (<p className="success-msg">Registration successful</p>) : ("")}
                    {loginError ? <p className="error-msg">Login invalid</p> : ""}    
            </div>    
        <div className={loggedIn ? "task-wrapper" : "hidden"}>
            <div className='header-wrapper'>
                <h1>Deine Aufgaben</h1>
            </div>
            <div className='header-wrapper'>
                <p>Du hast noch {openTasks} ausstehend Aufgaben</p>
            </div>
                
            <div className='create-wrapper'>
                <div className='input-wrapper'>
                <input type="text" placeholder='Neue Aufgabe...' ref={inputCreateRef} />
                <button className='btn' onClick={creating_task}>Erstellen</button>
            </div>
        </div>
            {tasks.map((item, index)=>{
                return (
                    <TaskElement
                    description={item.description}
                    done={item.done}
                    key={index}
                    onDeleteTask={delete_task}
                    onUpdateTask={update_Task}
                    id={item._id}
                    ></TaskElement>
                    )
                })}
            <div className="buttom-wrapper">
                <button className="btn" onClick={logout}>
                Logout
                </button>
            </div>  
        </div>
        </>
    )
}

export default List