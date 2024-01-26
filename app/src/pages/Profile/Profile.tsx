import { useAppSelector } from '@/hooks/useAppSelector';
import { useParams } from 'react-router-dom';
import OwnProfile from './OwnProfile';
import UserProfile from './UserProfile';

export default function Profile() {
  const { searchName } = useParams<{ searchName: string }>();
  const username = useAppSelector((state) => state.userReducer.username);

  return (
    <>
      {searchName === username ? (
        <OwnProfile />
      ) : (
        searchName && <UserProfile username={searchName} />
      )}
    </>
  );
}
