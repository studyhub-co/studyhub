import React from 'react'

import { Sheet } from '../../components/Sheet'

import classroomRoutes from '../../../../../../classroom/static/classroom/js/routes'
import classroomReducers from '../../../../../../classroom/static/classroom/js/reducers'
import useInjectReducer from '../../utils/reactHooks/useInjectReducer'

import requireAuthentication from '../../utils/requireAuthentication'

const ClassroomIndex = props => {
  // if you get warning in dev console here,
  // please see for detail: https://github.com/zalmoxisus/redux-devtools-extension/issues/759
  // inject async reducer
  Object.keys(classroomReducers).map((key, reducer) => {
    useInjectReducer({ key, reducer: classroomReducers[key] })
  })

  return (
    // class name needs for css separation
    <div className={'classroom'}>
      <Sheet>{classroomRoutes}</Sheet>
    </div>
  )
}

export default requireAuthentication(ClassroomIndex)
