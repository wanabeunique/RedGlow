import { Link } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faGear } from '@fortawesome/free-solid-svg-icons';

export default function ProfileSettingsLink() {
  return (
    <Link to="/settings" className="flex items-center gap-2 p-2 border rounded">
      <FontAwesomeIcon icon={faGear} />
      <p>Настройки</p>
    </Link>
  );
}
