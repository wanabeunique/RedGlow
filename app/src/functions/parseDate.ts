export interface IDate{
  year: number,
  month: string,
  day: number,
}

const months = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'];


export default function parseDate(date: string): IDate{
  const parsedDate: Date = new Date(date) 
    return {
      year: parsedDate.getFullYear(),
      month:  months[parsedDate.getMonth()],
      day: parsedDate.getDay()
    }
}
