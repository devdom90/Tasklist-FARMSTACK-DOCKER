import React from 'react';
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faTrash } from "@fortawesome/free-solid-svg-icons";


const TaskElement = ({description, done, id, onDeleteTask, onUpdateTask}) => {
  return (
   <>
    <div className={(done? "tasks--done" : "tasks--undone")}>
      <p onClick={() =>{onUpdateTask(id)}}>{description}</p>
      <p><FontAwesomeIcon
          icon={faTrash}
          onClick={() => {
            onDeleteTask(id);
          }}
        />
        </p>
    </div>
    </> 
  )
}

export default TaskElement