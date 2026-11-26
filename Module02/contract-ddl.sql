CREATE TABLE machine (
	machine_id INTEGER NOT NULL, 
	machine_name VARCHAR NOT NULL, 
	serial_no VARCHAR NOT NULL, 
	site VARCHAR NOT NULL, 
	installed DATE NOT NULL, 
	PRIMARY KEY (machine_id), 
	CONSTRAINT uq_machine_serial UNIQUE (serial_no), 
	CONSTRAINT ck_machine_id_positive CHECK (machine_id > 0), 
	CONSTRAINT ck_machine_serial_prefix CHECK (substr(serial_no, 1, 3) = 'SN-'), 
	UNIQUE (machine_name)
) ;

CREATE TABLE technician (
	technician_id INTEGER NOT NULL, 
	technician_name VARCHAR NOT NULL, 
	PRIMARY KEY (technician_id), 
	CONSTRAINT ck_technician_id_positive CHECK (technician_id > 0), 
	CONSTRAINT ck_technician_name_nonempty CHECK (length(trim(technician_name)) > 0)
) ;

CREATE TABLE part (
	part_no VARCHAR NOT NULL, 
	description VARCHAR NOT NULL, 
	unit_price NUMERIC(9, 2) NOT NULL, 
	PRIMARY KEY (part_no), 
	CONSTRAINT ck_part_price_nonnegative CHECK (unit_price >= 0)
) ;

CREATE TABLE maint_job (
	job_id INTEGER NOT NULL, 
	machine_id INTEGER NOT NULL, 
	technician_id INTEGER NOT NULL, 
	done_on DATE NOT NULL, 
	PRIMARY KEY (job_id), 
	CONSTRAINT ck_maint_job_id_positive CHECK (job_id > 0), 
	FOREIGN KEY(machine_id) REFERENCES machine (machine_id), 
	FOREIGN KEY(technician_id) REFERENCES technician (technician_id)
) ;

CREATE TABLE job_part (
	job_id INTEGER NOT NULL, 
	part_no VARCHAR NOT NULL, 
	PRIMARY KEY (job_id, part_no), 
	FOREIGN KEY(job_id) REFERENCES maint_job (job_id), 
	FOREIGN KEY(part_no) REFERENCES part (part_no)
) ;

