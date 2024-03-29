// import React from 'react'
//
// import PropTypes from 'prop-types'
// import { DragSource } from 'react-dnd'
// import { FaGripHorizontal, FaTimes } from 'react-icons/fa'
//
// import { DragItemTypes } from '../../../../dnd'
//
// export const dragSource = {
//   beginDrag (props) {
//     return { uuid: props.uuid }
//   }
// }
//
// function collect (connect, monitor) {
//   return {
//     connectDragSource: connect.dragSource(),
//     connectDragPreview: connect.dragPreview(),
//     isDragging: monitor.isDragging()
//   }
// }
//
// class MaterialThumbnailComponent extends React.Component {
//   constructor (props) {
//     super(props)
//     this.handleDeleteClick = this.handleDeleteClick.bind(this)
//   }
//   handleDeleteClick (e) {
//     e.preventDefault()
//     if (confirm('Are you sure you want to delete this material?')) {
//       this.props.onDeleteClick()
//     }
//   }
//
//   render () {
//     return this.props.connectDragPreview(
//       <div
//         className={
//           'question-thumbnail draggable' +
//           (this.props.selected ? ' selected' : '')
//         }
//         style={{ display: this.props.isDragging ? 'none' : 'block' }}
//         onClick={this.props.onClick}
//       >
//         <div className='question-thumbnail-inner'>
//           {this.props.connectDragSource(<span className='drag-handle'><FaGripHorizontal /></span>)}
//           <span>{this.props.shortText}</span>
//         </div>
//         <FaTimes className='btn-delete' onClick={this.handleDeleteClick} />
//       </div>
//     )
//   }
// }
//
// MaterialThumbnailComponent.propTypes = {
//   shortText: PropTypes.string,
//   onClick: PropTypes.func,
//   connectDragSource: PropTypes.func.isRequired,
//   connectDragPreview: PropTypes.func.isRequired,
//   onDeleteClick: PropTypes.func.isRequired,
//   isDragging: PropTypes.bool,
//   selected: PropTypes.bool
// }
//
// export const MaterialThumbnail = DragSource(DragItemTypes.MATERIAL, dragSource, collect)(
//   MaterialThumbnailComponent
// )
