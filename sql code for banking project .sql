



-- account details 

create proc [dbo].[account_details]
(
@aid  int
)
as
begin

select * from (select * from accountOpening where accountnumber=@aid) as n join   deposit as d on n.accountnumber=d.accountnumber
join withdraw as w
on n.accountnumber=w.accountnumber
join  runningbalance as r 
on n.accountnumber=r.accountnumber
end




-- account number 
create  proc [dbo].[account_number]
as
begin

select count(*) from accountOpening


end



-- Account opening money deposit
create proc [dbo].[account_opening_money_deposit]
(
@accountnumber  int,
@deposit_amount int ,
@date_of_deposit  varchar(40)
)
as
begin

insert into deposit values (@accountnumber,@deposit_amount,@date_of_deposit)

end



--- money balance  enquiry

create proc [dbo].[balance_enquiry]
(
@aid int
)
as
begin
select total_balance from runningbalance
where accountnumber=@aid

end

--check_balance

create proc [dbo].[check_balance]
(@acid  int
)
as
begin

select * from runningbalance
where accountnumber=@acid and total_balance>=100


end



-- check_money_transfer
create  proc [dbo].[check_money_transfer]
(
@accountnumber  int
)
as
begin

select total_balance from runningbalance
where accountnumber=@accountnumber


end




-- check_the_account_id_for_deposit

create  proc [dbo].[check_the_account_id_for_deposit]
(
@aid   varchar(40)
)
as
begin

select  count(accountnumber) from accountOpeningduplicate
where accountnumber=@aid

end



-- check_the_account_id_for_withdraw

create  proc [dbo].[check_the_account_id_for_withdraw]
(
@aid   varchar(40)
)
as
begin

select  count(accountnumber) from accountOpeningduplicate
where accountnumber=@aid

end



--  contact_number_verification_for_password_conformation

create proc [dbo].[contact_number_verification_for_password_conformation]
(
@contactnumber varchar(40)
)
as
begin
select count(*) from accountopeningduplicate 
where contactNumber=@contactnumber
end




-- delete_account

create proc [dbo].[delete_account]
(
@acid  int 
)
as
begin
DELETE FROM accountOpeningduplicate
WHERE accountNumber=@acid
end



-- details_delete
create proc [dbo].[details_delete]
(
@aid  int 
)
as
begin
DELETE FROM accountOpeningduplicate
WHERE accountnumber = @aid

end



-- find_accountnumber_by_using_the_receiver_phone_number


create proc [dbo].[find_accountnumber_by_using_the_receiver_phone_number]
(
@receiver_number  varchar(40)
)
as
begin
select accountnumber from accountopeningduplicate
where contactnumber=@receiver_number
end 



-- find_accountnumber_by_using_the_sender_phone_number

create proc [dbo].[find_accountnumber_by_using_the_sender_phone_number]
(
@sender_number  varchar(40)
)
as
begin
select accountnumber from accountopeningduplicate
where contactnumber=@sender_number
end 



-- forgat_and_update_password
create  proc [dbo].[forgat_and_update_password]
(
@contactnumber varchar(40),
@newpassword  varchar(40)
)
as
begin
UPDATE accountOpening
SET password_id=@newpassword
WHERE contactNumber=@contactnumber

UPDATE accountOpeningduplicate
SET password_id=@newpassword
WHERE contactNumber=@contactnumber

end



--insert_data_indeposit_for_amount_transfer_method

create  proc [dbo].[insert_data_indeposit_for_amount_transfer_method]
(
@account_number  int,
@money   int,
@date  varchar(40)
)
as
begin

insert into deposit values(@account_number,@money,@date )
end


-- insert_data_into_account_opening

create proc [dbo].[insert_data_into_account_opening]
(
@accountnumber	int,
@accountname  varchar(40),
@DOB	varchar(40),
@address varchar(40),
@contactNumber	varchar(40),
@account_opening_balance  int,
@account_opening_date  varchar(40),
@password  varchar(40)

)
as
begin
--create proc for insert the account opeming data in the table

insert into accountOpening values(@accountnumber,@accountname,@DOB,@address,@contactNumber,@account_opening_balance,@account_opening_date,@password)

insert into  accountOpeningduplicate values(@accountnumber,@accountname,@DOB,@address,@contactNumber,@account_opening_balance,@account_opening_date,@password)


end 




-- insert_data_inwithdarw_for_amount_transfer_method

create proc [dbo].[insert_data_inwithdarw_for_amount_transfer_method]
(
@account_number  int,
@money   int,
@date  varchar(40)
)
as
begin

insert into withdraw values(@account_number,@money,@date )
end



-- insert_delete_details
create proc [dbo].[insert_delete_details]
(
@acid  int,
@date varchar(40)

)
as
begin

insert into deleted_data values (@acid,@date)
end




-- money_sender_number

create proc [dbo].[money_sender_number]
(
@phone_number  varchar(40)
)
as
begin

select count(*)  from accountOpeningduplicate
where contactNumber=@phone_number
end 



-- only_money_deposit

create proc [dbo].[only_money_deposit]
(

@aid  int,
@deposit  int,
@date  varchar(40)
)
as
begin

insert into deposit values(@aid,@deposit,@date)


end



-- password_checking

create proc [dbo].[password_checking]
(
@aid  int
)
as
begin
select password_id from accountOpening
where accountnumber=@aid 

end 


-- password_conformation

create  proc [dbo].[password_conformation]
(
@contactnumber varchar(40)
)
as
begin
select password_id from accountopeningduplicate 
where contactNumber=@contactnumber
end




-- receiver_exit_or_not
create proc [dbo].[receiver_exit_or_not]
(
@receiver_number varchar(40)
)
as
begin
select count(*) from accountopeningduplicate
where contactnumber=@receiver_number
end 





-- running_balance

create   proc [dbo].[running_balance]
(
@accountnumber  int,
@deposit_amount int 
)
as
begin

insert into  runningbalance values (@accountnumber,@deposit_amount)

end



-- sender_exit_or_not
create proc [dbo].[sender_exit_or_not]
(
@sender_number  varchar(40)
)
as
begin
select count(*) from accountopeningduplicate
where contactnumber=@sender_number
end 




-- update_runnig_balance

create proc [dbo].[update_runnig_balance]
(
@aid   varchar(40),
@deposit  int
)
as
begin

		
		update  runningbalance
		set total_balance = total_balance+@deposit
		where accountnumber=@aid


end





-- update_withdrawmoney_in_runningbalance

create proc [dbo].[update_withdrawmoney_in_runningbalance]
(
@aid   int,
@withdrawmoney  int

)
as
begin

		update  runningbalance
		set total_balance = total_balance-@withdrawmoney
		where accountnumber=@aid


end







