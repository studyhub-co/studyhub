import { CHANGE_SELECTED_TAB, CHANGE_SELECTED_TAB_TEACHER_CLASSROOM } from '../constants'
// import history from '../history'
import { BASE_URL } from '../utils/config'

export function changeSelectedTab (selectedTab, tabNamespace, history, fromChildren = false) {
  if (!fromChildren) {
    history.push(BASE_URL + selectedTab + '/')
  }
  return { type: CHANGE_SELECTED_TAB,
    tab: selectedTab,
    namespace: tabNamespace }
}

export function changeTeacherClassroomSelectedTab (selectedTab, tabNamespace, history, match) {
  // TODO refactor this

  if (selectedTab === 'students') {
    if (match &&
      match.path !== '/classroom/teacher/:uuid/students/' &&
      match.path !== '/classroom/teacher/:uuid/students/:username') {
      history.push('/classroom/teacher/' + match.params['uuid'] + '/students/')
    }
  } else if (match &&
     !match.params.hasOwnProperty('assignmentUuid') &&
     !match.params.hasOwnProperty('username')
  ) { // main teacher page
    history.push('/classroom/teacher/' + match.params['uuid'] + '/')
  }

  // if (match &&
  //     match.isExact === false &&
  //     !match.params.hasOwnProperty('assignmentUuid') &&
  //     !match.params.hasOwnProperty('username') &&
  //     match.path !== '/classroom/:uuid/teacher/students/' &&
  //     match.path !== '/classroom/:uuid/teacher/' &&
  // {
  //   history.push('/classroom/' + match.params['uuid'] + '/teacher/') // rewrite url to teacher tab url. fixme: seems it's need a better solution
  // }

  return { type: CHANGE_SELECTED_TAB_TEACHER_CLASSROOM,
    teacherClassroomTab: selectedTab,
    namespace: tabNamespace
  }
}
