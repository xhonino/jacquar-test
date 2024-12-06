import './App.css';
import OutputNotificationList from './components/NotificationList';

function App() {
  return (
    <div className="bg-[#D8D8D8] h-screen flex flex-col items-center justify-center">
      <div className='w-[600px] flex justify-start'>
        <h1 className='text-xl p-4 text-gray-600'>
          ACTIVITY NOTIFICATIONS
        </h1>
      </div>
      <div className='h-[700px] w-[700px] bg-[#EFEFEF] flex flex-col'>
        <div className='w-full bg-[#095482] h-14 flex justify-end'>
          <div className='w-16 h-16 flex justify-center items-center mr-24'>
            <OutputNotificationList userId='2' />
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
