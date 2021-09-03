// <reference path="../../node_modules/dropbox/dist/dropbox.d.ts" /> // local verssion
/// <reference path="../../../../../../../../node_modules/dropbox/dist/dropbox.d.ts" /> // workspaces version
declare module 'dropbox_bridge' {
  export const Dropbox: typeof DropboxTypes.Dropbox
  export type Types = typeof DropboxTypes
}
