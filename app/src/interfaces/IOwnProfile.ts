import IProfile from "./IProfile"

export interface IOwnProfile extends IProfile{
  steamIdExists: boolean;
}